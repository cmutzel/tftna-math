# -*- coding: utf-8 -*-

import os
import pandas as pd

from openpyxl import load_workbook
from src.products.data_product import DataProduct

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PRODUCT_NAME = "daily_logs"

def get_trailing_value(row_values, field_name, max_cols=3):
    c=0
    value=None
    data_expected=False    
    for value in row_values: 
        if data_expected:
            if value is not None:
                value = value
                break
            elif c >= max_cols:
                break
            else:
                c = c + 1
        elif value == field_name:
            data_expected = True
        
    return value

def normalize_columns(frame):
    
    # fix all the columns names
    frame.columns = frame.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # now lets only take the columsn which have non-null names
    #  (i.e. carry forward no columns named '')
    final_columns = [name for name in frame.columns if name != '']
    
    return frame[final_columns]

class WeekyTrainingLog:
    def __init__(self):
        self.week_number = None
        self.target_hours = None
        self.nutrition_goal = None
        self.climbing_goal = None
        self.training_goal = None
        self.training_period = None
        
        self.column_labels_1 = []
        self.column_labels_2 = []
        self.final_column_labels = []
        self.daily_logs = []
        self.sheet_name = ""
        
    def __repr__(self):
        print "Week number: {}, Target Hours: {}, Training period: {}"
        
    def read_sheet(self, sheet):
        print "Reading sheet {}".format(sheet)
        wb = load_workbook(sheet)
        self.sheet = sheet
        sheet1 = wb["Sheet1"]
        
        for i, row in enumerate(sheet1.rows):
            
            # to save brainpower, align our loop index with the row numbers
            #  used in the spreadsheets, rather than 0-index counter
            r = i + 1
            
            row_values = [cell.value for cell in row]
            if r == 1:
                self.target_hours = get_trailing_value(row_values,
                "Target Hours this week:")
                
            if r == 3:
                self.week_number = get_trailing_value(row_values,
                "Week #")
                
            if r == 4:
                self.training_goal = get_trailing_value(row_values,
                "Training goal this week:")
                self.training_period = get_trailing_value(row_values,
                "Period:").lower().strip()
        
            if r == 5:
                self.climbing_goal = get_trailing_value(row_values,
                "Climbing goal this week:")        
        
            if r == 7:
                self.nutrition_goal = get_trailing_value(row_values,
                "Nutrition goals this week:")        
        
            if r == 10:
                self.column_labels_1 = row_values

            if r == 11:
                self.column_labels_2 = row_values

                
                """
                This next section of headers handles a mess due to the multi-level
                headers in the spreadsheets.  For some sections, the header is in the 
                first row, for some, in the second row, and for many, the column name 
                must be derived from an aggregation of the strings found in both rows. 
                """
                
                row1_label = ""
                row2_label = ""
                last_row1_label = ""
                for j in xrange(max(len(self.column_labels_1), len(self.column_labels_2))):
    
                    # we need to set a value for every column!    
                    if row1_label:
                        last_row1_label = row1_label
                    row1_label = self.column_labels_1[j]
                    row2_label = self.column_labels_2[j]
                    
                    if row1_label and not row2_label:
                        self.final_column_labels.append(row1_label)
                        
                    elif row1_label and row2_label:
                        self.final_column_labels.append(str(row1_label).lower() + str(row2_label).lower())
                        
                    elif not row1_label and row2_label:
                        self.final_column_labels.append(str(last_row1_label).lower() + str(row2_label).lower())
                        
                    elif not row1_label and not row2_label:
                        self.final_column_labels.append("")
    
                    else:
                        raise Exception("Failed to determine proper final column label from {} and {}".format(
                                row1_label, row2_label))
    
                # clean up the labels on our columns, which differ slightly between spreadsheets
                for k in xrange(len(self.final_column_labels)):
                      self.final_column_labels[k] = self.final_column_labels[k].replace(" by time", "_")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("time in intensity", "")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("zone", "zone_")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("/tour", "")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("hike/approach", "uphill")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("approach", "uphill")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("zone_1.0", "zone_1")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("zone_2.0", "zone_2")
                      self.final_column_labels[k] = self.final_column_labels[k].replace(".0", "")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("activity_altitude", "total_alt_gain")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("gained", "total_alt_gain")
                      self.final_column_labels[k] = self.final_column_labels[k].replace("altitude", "total_alt_gain")
                      
                self.final_column_labels.extend(["source", "training_period"])
        
            if r > 11 and r < 19:
                new_log_entry = row_values
                readable_sheet_name = self.sheet_name.replace("%2F", "/")
                new_log_entry.extend([readable_sheet_name, self.training_period])
                
                
                #logging.debug("Adding row {}".format(new_log_entry))
                self.daily_logs.append(new_log_entry)
            
    def to_dataframe(self): 
        logger.debug("Creating DataFrame with labels {}".format(
                self.final_column_labels))
        frame = pd.DataFrame.from_records(self.daily_logs,
                                          columns=self.final_column_labels)
        frame = frame.set_index(['Date'])
        frame = frame.fillna(value=0)
    
        return normalize_columns(frame)
    
    def get_column_names(self):
        return self.final_labels
     
    
class DailyLogs(DataProduct):
    product_name = PRODUCT_NAME
    requires = []
    
    def __init__(self, force_build_all=False):    
        super(DailyLogs, self).__init__(DailyLogs.product_name,
             force_build_all)
        
    def build(self):
        path_to_data = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "../../data/raw/")
        logs = os.listdir(path_to_data)
        all_frames = []
        for log in logs:
            if "Log" in log:
                weeklyLog = WeekyTrainingLog()
                weeklyLog.read_sheet(path_to_data + log)
                frame = weeklyLog.to_dataframe()
                
                logger.debug("Adding {} logs with with dates {} through {}".format(
                        len(frame), min(frame.index), max(frame.index)))
                all_frames.append(frame)
                #break    
                
        return pd.concat(all_frames)
    
    def verify(daily_logs):
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
        daily_logs = daily_logs.sort_index()
        
        logger.debug("First date in range: {}".format(min(daily_logs.index)))
        logger.debug("Last date in range: {}".format(max(daily_logs.index)))
        
        grouped_on_date = daily_logs.groupby(level=0)
        duplicate_rows = grouped_on_date.size()[lambda i: i > 1]
        
        logger.warning("Found {} duplicate rows...".format(len(duplicate_rows)))
        if len(duplicate_rows) > 0:
            logging.warning(duplicate_rows)
        
        return daily_logs
    