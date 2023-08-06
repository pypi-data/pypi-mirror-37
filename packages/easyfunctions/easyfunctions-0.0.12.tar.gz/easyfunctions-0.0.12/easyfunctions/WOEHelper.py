import re
import pandas as pd
import numpy as np


class WOEHelper:

    def __init__(self):
        self.verbose = True
        self.labels = {   'WOE' : 'W.O.E.',
                          'distribution' : 'Distribution',
                          'g_distribution' : 'Good Dist',
                          'b_distribution' : 'Bad Dist',
                          'iv' : 'I.V.',
                          'g_prob' : 'Good Rate',
                          'b_prob' : 'Bad Rate',
                          'cum_zeros' : 'Accum 0',
                          'cum_ones' : 'Accum 1',
                          'total' : 'Total',
                          'accum_total' : 'Total Cum',
                          'odds' : 'Odds',
                          'ks' : 'K.S.',
                          'gini' : 'Gini',
                          'diff' : 'Diff'}


    def setVerbose(self, in_value):
        self.verbose = in_value
        if in_value:
            print('Verbose set to on. Messages will be printed.')
        else:
            print('Verbose set to off. No messages will be printed.')


    def setLabel(self, entry, value):
        self.labels[entry] = value


    def getInformationValue(self, df_in, independent_feature, dependent_feature):

        table = pd.crosstab(index=df_in[independent_feature], columns=df_in[dependent_feature], margins=True)

        total_A = table.tail(1).iloc[0,2]
        table[self.labels['distribution']] = table.iloc[:,2:3]/total_A

        total_B = table.tail(1).iloc[0,0]
        table[self.labels['g_distribution']] = table.iloc[:,0:1]/total_B

        total_M = table.tail(1).iloc[0,1]

        table[self.labels['b_distribution']] = table.iloc[:,1:2]/total_M

        table[self.labels['iv']] = (table[self.labels['g_distribution']] - table[self.labels['b_distribution']]) * np.log(table[self.labels['g_distribution']] / table[self.labels['b_distribution']])

        table[self.labels['WOE']] = np.log(table[self.labels['g_distribution']] / table[self.labels['b_distribution']]) * 100
        
        table.iloc[-1:,6] = table[self.labels['iv']].iloc[:-1].sum(axis=0)

        table[self.labels['g_prob']] = table[1] / table['All']
        table[self.labels['b_prob']] =  table[0] / table['All']

        table.iloc[-1:,7] = ''
        table.iloc[-1:,5] = ''
        table.iloc[-1:,4] = ''
        table.iloc[-1:,3] = ''
        table.iloc[-1:,8] = ''
        table.iloc[-1:,9] = ''

        return table
        
        
    def WOEvaluation(self, df_in, woe_evaluation_var, target):

        ks_table = pd.crosstab(index = df_in[woe_evaluation_var], columns = df_in[target])

        ks_table[self.labels['cum_zeros']]          =       (ks_table[0].cumsum()) / ks_table[0].sum()

        ks_table[self.labels['cum_ones']]           =       (ks_table[1].cumsum()) / ks_table[1].sum()

        ks_table[self.labels['total']]              =       ks_table[0]+ks_table[1]
        
        ks_table[self.labels['accum_total']]        =       (ks_table[self.labels['total']].cumsum()) / ks_table[self.labels['total']].sum()

        ks_table[self.labels['odds']]               =       ks_table[0] / ks_table[1]
        
        ks_table[self.labels['ks']]                 =       abs(ks_table[self.labels['cum_zeros']] - ks_table[self.labels['cum_ones']])

        ks_table['Accum_men']                       =       ks_table[self.labels['cum_zeros']].shift()
        
        ks_table.iloc[0,8]                          =       0
        
        ks_table['Accum_suma_buenos']               =       ks_table[self.labels['cum_zeros']] + ks_table['Accum_men']

        ks_table[self.labels['diff']]               =       ks_table[self.labels['cum_ones']].diff()
        
        ks_table.iloc[0,10]                         =       ks_table.iloc[0,3]
        
        ks_table[self.labels['gini']]               =       ks_table['Accum_suma_buenos'] * ks_table[self.labels['diff']]

        ks_table.reset_index()
        
        KS_final                                    =       ks_table[[0,1,self.labels['cum_zeros'],self.labels['cum_ones'],self.labels['total'],self.labels['accum_total'],self.labels['odds'],self.labels['ks'],self.labels['gini']]]

        d = { self.labels['ks'] : [round(max(ks_table[self.labels['ks']]),3)], self.labels['gini'] : [round(abs((1 - sum(ks_table[self.labels['gini']]))),3)] , self.labels['roc']: [round(((abs(1 - sum(ks_table[self.labels['gini']])) + 1) / 2), 3)]}
        
        df = pd.DataFrame(data=d)

        return df


    def catSplit(self, df_in, var_name, in_cut_points):
        
        cols_to_max = list()
        count = 1
        
        for cut_point in in_cut_points:
            df_in['cat_' + str(count) + '_' + var_name] = df_in[var_name].apply(lambda x: count if x >= cut_point else 0)
            cols_to_max.append('cat_' + str(count) + '_' + var_name)
            count += 1
        
        df_in['cat_' + var_name] = df_in[cols_to_max].max(axis=1)
        df_in.drop(cols_to_max, axis=1, inplace=True)
        WOE = getInformationValue(df_in,'cat_' + var_name, 'churn')
        WOE2 = WOE.reset_index()
        
        #plot
        
        fig, ax = plt.subplots()
        ax.plot(WOE2['cat_'+ var_name].iloc[0:count-1], WOE2[self.labels['WOE']].iloc[0:count-1])
        
        #WOE var creation
        
        cols_to_max = list()
        count = 1
         
        for woe in WOE[self.labels['WOE']]:
            df_in['WOE_' + str(count) + '_' + var_name] = df_in['cat_' + var_name].apply(lambda x: woe if x == count else -float('Inf'))
            cols_to_max.append('WOE_' + str(count) + '_' + var_name)
            count += 1
        
        df_in['WOE_' + var_name] = df_in[cols_to_max].max(axis=1)
        df_in.drop(cols_to_max, axis=1, inplace=True)

        if self.verbose:
            print('catSplit -- ' + labels['WOE'] + ' value counts:')
            print(df_in['WOE_' + var_name].value_counts())
        
        return WOE





