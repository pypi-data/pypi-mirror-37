"""
*******************************************************
 * Copyright (C) 2017 MindsDB Inc. <copyright@mindsdb.com>
 *
 * This file is part of MindsDB Server.
 *
 * MindsDB Server can not be copied and/or distributed without the express
 * permission of MindsDB Inc
 *******************************************************
"""

import mindsdb.config as CONFIG
from mindsdb.libs.constants.mindsdb import *
from mindsdb.libs.phases.base_module import BaseModule
from mindsdb.libs.helpers.logging import logging
from mindsdb.libs.data_types.transaction_metadata import TransactionMetadata

from collections import OrderedDict

import sys
import json
import random
import traceback
import sqlite3
import pandas
import json



class DataExtractor(BaseModule):

    phase_name = PHASE_DATA_EXTRACTION

    def populatePredictQuery(self):

        # If its a predict function
        # Create a query statement where data can be pulled from
        # for now we can just populate the when statement in a select queryt
        # TODO: combine WHEN and WHERE

        # make when_conditions a list of dictionaries
        if type(self.transaction.metadata.model_when_conditions) != type([]):
            when_conditions = [self.transaction.metadata.model_when_conditions]
        else:
            when_conditions = self.transaction.metadata.model_when_conditions

        # these are the columns in the model, pulled from persistent_data
        columns = self.transaction.persistent_model_metadata.columns  # type: list

        when_conditions_list = []
        # here we want to make a list of the type  ( ValueForField1, ValueForField2,..., ValueForFieldN ), ...
        for when_condition in when_conditions:
            cond_list = ["NULL"] * len(columns)  # empty list with blanks for values

            for condition_col in when_condition:
                col_index = columns.index(condition_col)
                cond_list[col_index] = when_condition[condition_col]

            when_conditions_list.append(cond_list)

        # create the strings to be populated in the query as follows
        values_string = ",\n ".join(
            ["({val_string})".format(val_string=", ".join([str(val) for val in when_condition])) for when_condition in
             when_conditions_list])
        fields_string = ', '.join(
            ['column{i} as {col_name}'.format(i=i + 1, col_name=col_name) for i, col_name in enumerate(columns)])

        query = '''
                    select
                        {fields_string}

                    from (
                        values
                            {values_string}
                    ) 

                    '''.format(fields_string=fields_string, values_string=values_string)

        self.session.logging.info('Making PREDICT from query: {query}'.format(query=query))
        self.transaction.metadata.model_query = query

    def prepareFullQuery(self, train_metadata):

        if train_metadata.model_order_by:
            order_by_fields = train_metadata.model_order_by if train_metadata.model_group_by is None else [train_metadata.model_group_by] + train_metadata.model_order_by
        else:
            order_by_fields = []


        order_by_string = ", ".join(["{oby} {type}".format(oby=oby, type=DEFAULT_ORDER_BY_TYPE) for oby in order_by_fields])

        where_not_null_string = ''
        if train_metadata.model_ignore_null_targets and self.transaction.metadata.type != TRANSACTION_PREDICT:
            not_null_conditions = " AND ".join([" {col} IS NOT NULL ".format(col=t_col) for t_col in self.transaction.metadata.model_predict_columns])
            where_not_null_string = 'WHERE {not_null_conditions} '.format(not_null_conditions=not_null_conditions)

        if len(order_by_fields):
            query_wrapper = '''select * from ({orig_query}) orgi {where_not_null_string} order by {order_by_string}'''
        else:
            query_wrapper = '''select * from ({orig_query}) orgi {where_not_null_string} '''

        query = query_wrapper.format(orig_query=train_metadata.model_query, order_by_string=order_by_string,
                                     where_not_null_string=where_not_null_string)

        return query

    def run(self):

        # Handle transactions differently depending on the type of query
        # For now we only support LEARN and PREDICT

        train_metadata = self.transaction.metadata

        if self.transaction.metadata.type == TRANSACTION_PREDICT:

            self.populatePredictQuery()

            train_metadata = TransactionMetadata()
            train_metadata.setFromDict(self.transaction.persistent_model_metadata.train_metadata)

        elif self.transaction.metadata.type not in [TRANSACTION_PREDICT, TRANSACTION_LEARN]:

            self.session.logging.error('Do not support transaction {type}'.format(type=self.transaction.metadata.type))
            self.transaction.error = True
            self.transaction.errorMsg = traceback.print_exc(1)
            return



        query = self.prepareFullQuery(train_metadata)

        try:
            self.transaction.session.logging.info('About to pull query {query}'.format(query=query))
            conn = sqlite3.connect(self.transaction.metadata.storage_file)
            self.logging.info(self.transaction.metadata.model_query)
            df = pandas.read_sql_query(query, conn)
            result = df.where((pandas.notnull(df)), None)
            df = None # clean memory

        except Exception:

            self.session.logging.error(traceback.print_exc())
            self.transaction.error =True
            self.transaction.errorMsg = traceback.print_exc(1)
            return

        columns = list(result.columns.values)
        data_array = list(result.values.tolist())

        self.transaction.input_data.columns = columns

        if len(data_array[0])>0 and  self.transaction.metadata.model_predict_columns:
            for col_target in self.transaction.metadata.model_predict_columns:
                if col_target not in self.transaction.input_data.columns:
                    err = 'Trying to predict column {column} but column not in source data'.format(column=col_target)
                    self.session.logging.error(err)
                    self.transaction.error = True
                    self.transaction.errorMsg = err
                    return

        self.transaction.input_data.data_array = data_array

        # extract test data if this is a learn transaction and there is a test query
        if self.transaction.metadata.type == TRANSACTION_LEARN:

            if self.transaction.metadata.model_test_query:
                try:
                    test_query = query_wrapper.format(orig_query = self.transaction.metadata.model_test_query, order_by_string= order_by_string, where_not_null_string=where_not_null_string)
                    self.transaction.session.logging.info('About to pull TEST query {query}'.format(query=test_query))
                    #drill = self.session.drill.query(test_query, timeout=CONFIG.DRILL_TIMEOUT)
                    df = pandas.read_sql_query(test_query, conn)
                    result = df.where((pandas.notnull(df)), None)
                    df = None

                    #result = vars(drill)['data']
                except Exception:

                    # If testing offline, get results from a .cache file
                    self.session.logging.error(traceback.print_exc())
                    self.transaction.error = True
                    self.transaction.errorMsg = traceback.print_exc(1)
                    return

                columns = list(result.columns.values)
                data_array = result.values.tolist()

                # Make sure that test adn train sets match column wise
                if columns != self.transaction.input_data.columns:
                    err = 'Trying to get data for test but columns in train set and test set dont match'
                    self.session.logging.error(err)
                    self.transaction.error = True
                    self.transaction.errorMsg = err
                    return
                total_data_array = len(self.transaction.input_data.data_array)
                total_test_array =  len(data_array)
                test_indexes = [i for i in range(total_data_array, total_data_array+total_test_array)]

                self.transaction.input_data.test_indexes = test_indexes
                # make the input data relevant
                self.transaction.input_data.data_array += data_array

                # we later use this to either regenerate or not
                test_prob = 0

            else:
                test_prob = CONFIG.TEST_TRAIN_RATIO

            validation_prob = CONFIG.TEST_TRAIN_RATIO / (1-test_prob)

            group_by = self.transaction.metadata.model_group_by

            if group_by:
                try:
                    group_by_index = self.transaction.input_data.columns.index(group_by)
                except:
                    group_by_index = None
                    err = 'Trying to group by, {column} but column not in source data'.format(column=group_by)
                    self.session.logging.error(err)
                    self.transaction.error = True
                    self.transaction.errorMsg = err
                    return

                # get unique group by values
                all_group_by_items_query = ''' select {group_by_column} as grp, count(1) as total from ( {query} ) sub group by {group_by_column}'''.format(group_by_column=group_by, query=self.transaction.metadata.model_query)
                self.transaction.session.logging.debug('About to pull GROUP BY query {query}'.format(query=all_group_by_items_query))
                df = pandas.read_sql_query(all_group_by_items_query, conn)
                result = df.where((pandas.notnull(df)), None)
                # create a list of values in group by, this is because result is array of array we want just array

                all_group_by_counts = {i[0]:i[1] for i in result.values.tolist()}
                all_group_by_values = all_group_by_counts.keys()

                max_group_by = max(list(all_group_by_counts.values()))

                self.transaction.persistent_model_metadata.max_group_by_count = max_group_by

                # we will fill these depending on the test_prob and validation_prob
                test_group_by_values = []
                validation_group_by_values = []
                train_group_by_values = []

                # split the data into test, validation, train by group by data
                for group_by_value in all_group_by_values:

                    # depending on a random number if less than x_prob belongs to such group
                    # remember that test_prob can be 0 or the config value depending on if the test test was passed as a query
                    if float(random.random()) < test_prob and len(train_group_by_values) > 0:
                        test_group_by_values += [group_by_value]
                    # elif float(random.random()) < validation_prob:
                    #     validation_group_by_values += [group_by_value]
                    else:
                        train_group_by_values += [group_by_value]

            for i, row in enumerate(self.transaction.input_data.data_array):

                in_test = True if i in self.transaction.input_data.test_indexes else False
                if not in_test:
                    if group_by:

                        group_by_value = row[group_by_index]
                        if group_by_value in test_group_by_values :
                            self.transaction.input_data.test_indexes += [i]
                        elif group_by_value in train_group_by_values :
                            self.transaction.input_data.train_indexes += [i]
                        elif group_by_value in validation_group_by_values :
                            self.transaction.input_data.validation_indexes += [i]

                    else:
                        # remember that test_prob can be 0 or the config value depending on if the test test was passed as a query
                        if float(random.random()) <= test_prob or len(self.transaction.input_data.test_indexes) == 0:
                            self.transaction.input_data.test_indexes += [i]
                        elif float(random.random()) <= validation_prob or len(self.transaction.input_data.validation_indexes)==0:
                            self.transaction.input_data.validation_indexes += [i]
                        else:
                            self.transaction.input_data.train_indexes += [i]

            if len(self.transaction.input_data.test_indexes) == 0:
                logging.debug('Size of test set is zero, last split')
                ratio = CONFIG.TEST_TRAIN_RATIO
                if group_by and len(self.transaction.input_data.train_indexes) > 2000:
                    # it seems to be a good practice to not overfit, to double the ratio, as time series data tends to be abundant
                    ratio = ratio*2
                test_size = int(len(self.transaction.input_data.train_indexes) * ratio)
                self.transaction.input_data.test_indexes = self.transaction.input_data.train_indexes[-test_size:]
                self.transaction.input_data.train_indexes = self.transaction.input_data.train_indexes[:-test_size]

            logging.info('- Test: {size} rows'.format(size=len(self.transaction.input_data.test_indexes)))
            logging.info('- Train: {size} rows'.format(size=len(self.transaction.input_data.train_indexes)))


def test():
    from mindsdb.libs.controllers.mindsdb_controller import MindsDBController as MindsDB

    mdb = MindsDB()
    mdb.learn(from_query='select * from position_target_table', group_by = 'id', order_by=['max_time_rec'], predict='position', model_name='mdsb_model', test_query=None, breakpoint = PHASE_DATA_EXTRACTION)

# only run the test if this file is called from debugger
if __name__ == "__main__":
    test()

