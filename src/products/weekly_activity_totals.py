# -*- coding: utf-8 -*-
"""
weekly-activity-totals.py

Created on Tue Feb  7 19:08:14 2017

@author: chrismutzel
"""
import numpy as np
from src.products.data_product import DataProduct

"""make this visible at the top of the file for easier reading"""
PRODUCT_NAME = "weekly_activity_totals"

class WeeklyActivityTotals(DataProduct):
    product_name = PRODUCT_NAME
    requires = ["daily_logs"]

    def __init__(self, force_build_all=False):
        super(WeeklyActivityTotals, self).__init__(
                WeeklyActivityTotals.product_name, force_build_all)
        
    def build(self):
        """
        Computes total hours for each activity on a weekly basis, and 
    
        Parameters
        ----------
        daily_logs : Pandas.DataFrame where each row is a training day. 
            See get_daily_logs_as_dataframe
    
        Returns
        -------
        Pandas.DataFrame with week # as index (i.e. 1-N).  Frame includes a column
        with sum of hours for each activity each week and also a column showing
        total of training hours. 
        i.e. 
            activity_bike  activity_run activity_climb  total
        1             0.5             1              0    1.5 
        2               0             1              1      2 
        ...
        
        """
    
        # lets count up the weekly totals
        daily_logs = self.daily_logs.reset_index() #we want to preserve the date 
        daily_logs["week"] = daily_logs["Date"].map(lambda t: t.week)
        grouped_byweek = daily_logs.groupby(["week"])
        cols = [c for c in daily_logs.columns if ("activity_" in c or "zone" in c)]
        
        min_dates = grouped_byweek.agg({"Date" : np.min})
        sum_activities = grouped_byweek.sum()[cols]
        sum_activities["total"] = sum_activities.apply(np.sum, axis=1)
        
        # we need to reset the index, as our training period may have
        #  started before the new year, in which case the first few weeks of 
        #  training actually have a week = 54, 55, 56 ...
        weekly_totals = min_dates.join(sum_activities)
        a = [0 for i in xrange(24)]
        a.extend([-53, -53, -53, -53, -53])
        new_index = np.array([sum_activities.index.values + a]) + 4
        weekly_totals.index = new_index[0]
        
        return weekly_totals.sort_index()
    

    def verify(self):
        """
            Runs a few basic tests on our data after we have done some munging.
            Returns unmodifed inputs if data is verified, otherwise
            an exception is thrown.
            
            Parameters
            ----------
            daily_logs : Pandas.DataFrame where each row is a training day. 
                See get_daily_logs_as_dataframe
        
            Returns
            -------
            daily_logs as passed into Parameters
        """
        
        # some quick checks on the data
        daily_logs = self.values
        daily_logs = daily_logs.sort_index()
        
        print "First date in range: {}".format(min(daily_logs.index))
        print "Last date in range: {}".format(max(daily_logs.index))
        
        grouped_on_date = daily_logs.groupby(level=0)
        duplicate_rows = grouped_on_date.size()[lambda i: i > 1]
        
        print "Found {} duplicate rows...".format(len(duplicate_rows))
        if len(duplicate_rows) > 0:
            print duplicate_rows    
        
        return daily_logs
    