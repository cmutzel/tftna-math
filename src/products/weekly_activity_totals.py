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
            activity_bike  activity_run activity_climb  total training_period
        1             0.5             1              0    1.5      transition
        2               0             1              1      2      transition       
        ...
        n               1             0              2      1            base       
        
        """
    
        # used pandas group by to get the sum for each intensity tye and
        #  activity for each week.  Keep track of the date
        #   and the training period
        daily_logs = self.daily_logs.reset_index() #we want to preserve the date 
        daily_logs["week"] = daily_logs["Date"].map(lambda t: t.week)

        cols = [c for c in daily_logs.columns if ("activity_" in c or "zone" in c)]
        funcs = {}
        funcs["Date"] = np.min
        funcs["training_period"] = lambda x: x.iloc[0] # ~= first()
        for c in cols:
            funcs[c] = np.sum
                        
        grouped_byweek = daily_logs.groupby(["week"])
        return grouped_byweek.agg(funcs).sort_values(by=["Date"]).reset_index()

    def verify(self):   
        return self.value
    
if __name__ == "__main__":
    from src.products.product_factory import DataProductFactory
    factory = DataProductFactory()
    value = factory.get_product(PRODUCT_NAME, force_build=True)
    print value