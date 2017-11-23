# -*- coding: utf-8 -*-
import scipy.stats
import numpy as np

class DescriptiveStatistics():

    def calculate_ave_var_cv(self,data_I,confidence_I = 0.95):
        """calculate the average, var, %cv of data
        with 95% confidence intervals"""

        try:
            data = np.array(data_I)

            data_ave_O = 0.0
            # calculate the average of the sample
            data_ave_O = np.mean(data)

            data_var_O = 0.0
            #calculate the variance of the sample
            data_var_O = np.var(data)

            #calculate the standard error of the sample
            se = scipy.stats.sem(data)

            #calculate the CV% of the sample
            data_cv_O = 0.0
            if data_ave_O !=0.0:
                data_cv_O = np.std(data)/data_ave_O*100

            #calculate the 95% confidence intervals
            n = len(data)
            h = se * scipy.stats.t._ppf((1+confidence_I)/2., n-1)
            data_lb_O = data_ave_O - h
            data_ub_O = data_ave_O + h

            return data_ave_O, data_var_O, data_cv_O, data_lb_O, data_ub_O
        except Exception as e:
            print(e)
            exit(-1)

    def calculate_interquartiles(self,data_I,iq_range_I = [25,75]):
        '''compute the interquartiles and return the min, max, median, iq1 and iq3'''
        try:
            min_O = np.min(data_I)
            max_O = np.max(data_I)
            iq_1_O, iq_2_O = np.percentile(data_I, iq_range_I)
            median_O = np.median(data_I)

            return min_O, max_O, median_O, iq_1_O, iq_2_O
        except Exception as e:
            print(e)

    def calculate_descriptiveStats(self,
            data_I,
            confidence_I = 0.95,
            iq_range_I = [25,75]):
        '''calculate the mean, var, cv, 95% CI,
        min, max, median, and IQ ranges for the data
        Args:
            data_I = array of data points

        Returns:
            dict: descriptiveStats_O
        '''
        descriptiveStats_O = None
        try:
            mean,var,cv,lb,ub = self.calculate_ave_var_cv(data_I,confidence_I =confidence_I)
            min, max, median, iq_1, iq_3 = self.calculate_interquartiles(data_I,iq_range_I=iq_range_I)
            descriptiveStats_O = {
                'n':len(data_I),
                'mean':mean,
                'var':var,
                'cv':cv,
                'ci':confidence_I,
                'lb':lb,
                'ub':ub,
                'min':min,
                'max':max,
                'median':median,
                'iq_1':iq_1,
                'iq_3':iq_3,
                'iq':iq_range_I}
        except Exception as e:
            print(e)
            descriptiveStats_O = {
                'n':len(data_I),
                'mean':None,
                'var':None,
                'cv':None,
                'ci':confidence_I,
                'lb':None,
                'ub':None,
                'min':None,
                'max':None,
                'median':None,
                'iq_1':None,
                'iq_3':None,
                'iq':iq_range_I}
        return descriptiveStats_O