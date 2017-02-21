# -*- coding: utf-8 -*-
"""
weekly-activity-totals.py

Created on Tue Feb  7 19:08:14 2017

@author: chrismutzel
"""
import numpy as np
from src.products.data_product import DataProduct
PRODUCT_NAME = "weekly_activity_totals"

class WeeklyActivityTotals(DataProduct):
    product_name = PRODUCT_NAME
    requires = ["daily_logs"]

    def __init__(self):
        super(WeeklyActivityTotals, self).__init__(
                WeeklyActivityTotals.product_name)
        
    def build(self):
        """
        Computes total hours for each activity on a weekly basis, and 
    
        Parameters
        ----------
        None
    
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
        #period = grouped_byweek.agg({""})
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
        return self.value
    
if __name__ == "__main__":
    from src.products.product_factory import DataProductFactory
    factory = DataProductFactory()
    value = factory.get_product(PRODUCT_NAME, force_build=True)
    print value