import re
import pandas as pd
import numpy as np


class pandasDataFrameManipulator:


    def __init__(self):
        self.verbose = True
        self.list_of_columns = []
        self.list_of_exceptions = []


    def setVerbose(self, in_value):
        self.verbose = in_value
        if in_value:
            print('Verbose set to on. Messages will be printed.')
        else:
            print('Verbose set to off. No messages will be printed.')


    def eliminateNullFeatures(self, df_in, threshold):
        if self.verbose:
            print('eliminateNullFeatures Results:\n--------------------------------------------------------')

        nulls = df_in.isnull().sum()
        nulls = nulls.reset_index()
        nulls.columns = ['feature','null_count']
        nulls['null_perc'] = nulls['null_count'] / df_in.shape[0]
        features_to_eliminate = nulls[nulls['null_perc'] >= threshold]['feature'].tolist()
        if len(features_to_eliminate) > 0:
            df_in.drop(features_to_eliminate,inplace=True, axis=1)
            if self.verbose:
                print(str(len(features_to_eliminate)) + ' features were eliminated from DataFrame: ') 
                [print(feature) for feature in features_to_eliminate]
        else:
            if self.verbose:
                print('0 features were eliminated')
           
        return df_in


    def getDataFrameSegmentByReExp(self, df_in, list_of_columns=[], list_of_exceptions=[], use_last_lists=False, reset_index=True, drop_columns=False):

        if use_last_lists:
            list_of_columns = self.list_of_columns
        else:
            self.list_of_columns = list_of_columns
        if use_last_lists:
            list_of_exceptions = self.list_of_exceptions
        else:
            self.list_of_exceptions = list_of_exceptions


        if self.verbose:
            print('getDataFrameSegmentByReExp Results:\n--------------------------------------------------------')

        output_cols = list()
        cols = df_in.columns.values
        for i in list_of_columns:
            pattern = re.compile(i)
            for col in cols:
                exclude = False
                for exc in list_of_exceptions:
                        exc_pattern = re.compile(exc)
                        if re.match(pattern=exc_pattern, string=col):
                            exclude = True
                if exclude == False:
                    if re.match(pattern=pattern, string=col):
                        output_cols.append(col)
        df_out = df_in[output_cols]
        if self.verbose:
            print(str(len(output_cols)) + ' columns filtered out from input DataFrame:')
            [print(col) for col in output_cols]
        if reset_index:
            df_out.set_index(np.arange(len(df_out)),inplace=True)
            if self.verbose:
                print('Index was reseted')
        if drop_columns:
            df_in.drop(output_cols, inplace=True, axis=1)
            if self.verbose:
                print('Filtered out columns were dropped from input DataFrame')

        return df_out


    def dropColumnsFromDataFrame(self, df_in, list_of_columns=[], list_of_exceptions=[], use_last_lists=False):

        if use_last_lists:
            list_of_columns = self.list_of_columns
        else:
            self.list_of_columns = list_of_columns
        if use_last_lists:
            list_of_exceptions = self.list_of_exceptions
        else:
            self.list_of_exceptions = list_of_exceptions

        if self.verbose:
            print('dropColumnsFromDataFrame Results:\n--------------------------------------------------------')

        cols = df_in.columns.values
        cols_to_drop = list()
        for i in list_of_columns:
            pattern = re.compile(i)
            for col in cols:
                exclude = False
                for exc in list_of_exceptions:
                    exc_pattern = re.compile(exc)
                    if re.match(pattern=exc_pattern, string=col):
                        exclude = True
                if exclude == False:
                    if re.match(pattern=pattern, string=col):
                        cols_to_drop.append(col)
        df_in.drop(cols_to_drop, inplace=True, axis=1)
        if self.verbose:
            print(str(len(cols_to_drop)) + ' dropped from input DataFrame:')
            [print(col) for col in cols_to_drop]
        
        return df_in


    def sumByReExp(self, df_in, result_column_name, list_of_columns=[], list_of_exceptions=[], use_last_lists=False, drop_columns=False):

        if use_last_lists:
            list_of_columns = self.list_of_columns
        else:
            self.list_of_columns = list_of_columns
        if use_last_lists:
            list_of_exceptions = self.list_of_exceptions
        else:
            self.list_of_exceptions = list_of_exceptions

        if self.verbose:
            print('sumByReExp Results:\n--------------------------------------------------------')

        cols = df_in.columns.values
        cols_to_sum = list()
        df_in[result_column_name] = 0
        for i in list_of_columns:
            pattern = re.compile(i)
            for col in cols:
                exclude = False
                for exc in list_of_exceptions:
                    exc_pattern = re.compile(exc)
                    if re.match(pattern=exc_pattern, string=col):
                        exclude = True
                if exclude == False:
                    if re.match(pattern=pattern, string=col):
                        cols_to_sum.append(col)
                        df_in[result_column_name] += df_in[col]
        if self.verbose:
            print(str(len(cols_to_sum)) + ' added into ' + result_column_name + ':')
            [print(col) for col in cols_to_sum]
        if drop_columns:
            df_in.drop(cols_to_sum, inplace=True, axis=1)
            if self.verbose:
                print('Summarized columns were dropped from input DataFrame')
            
        return df_in

    def maxByReExp(self, df_in, result_column_name, list_of_columns=[], list_of_exceptions=[], use_last_lists=False, drop_columns=False):

        if use_last_lists:
            list_of_columns = self.list_of_columns
        else:
            self.list_of_columns = list_of_columns
        if use_last_lists:
            list_of_exceptions = self.list_of_exceptions
        else:
            self.list_of_exceptions = list_of_exceptions

        if self.verbose:
            print('maxByReExp Results:\n--------------------------------------------------------')

        cols = df_in.columns.values
        cols_to_max = list()
        for i in list_of_columns:
            pattern = re.compile(i)
            for col in cols:
                exclude = False
                for exc in list_of_exceptions:
                    exc_pattern = re.compile(exc)
                    if re.match(pattern=exc_pattern, string=col):
                        exclude = True
                if exclude == False:
                    if re.match(pattern=pattern, string=col):
                        cols_to_max.append(col)
        df_in[result_column_name] = df_in[cols_to_max].max(axis=1)
        if self.verbose:
            print(str(len(cols_to_max)) + ' taken to find max value into ' + result_column_name + ':')
            [print(col) for col in cols_to_max]
        if drop_columns:
            df_in.drop(cols_to_max, inplace=True, axis=1)
            if self.verbose:
                print('Summarized columns were dropped from input DataFrame')
            
        return df_in


    def calculateEvolutionByRegExp(self, df_in, comparison_column, result_column_name, list_of_columns=[], list_of_exceptions=[], use_last_lists=False, drop_columns=False):

        if use_last_lists:
            list_of_columns = self.list_of_columns
        else:
            self.list_of_columns = list_of_columns
        if use_last_lists:
            list_of_exceptions = self.list_of_exceptions
        else:
            self.list_of_exceptions = list_of_exceptions

        if self.verbose:
            print('calculateEvolutionByRegExp Results:\n--------------------------------------------------------')

            self.maxByReExp(df_in, list_of_columns, 'tmp_max_' + result_column_name, drop_columns=False)

            df_in[result_column_name] = df_in[comparison_column] / df_in['tmp_max_' + result_column_name]

            if drop_columns:
                temp_column_pattern = '^tmp_max_' + result_column_name + '$'
                comparison_column_pattern = '^' + comparison_column + '$'
                self.dropColumnsFromDataFrame(df_in, [temp_column_pattern] + list_of_columns, [comparison_column_pattern]) 

        return df_in

