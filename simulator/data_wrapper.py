from optparse import Values
import pandas as pd
import numpy as np
import glob
import os
from datetime import timezone
import pytz

class data_wrapper:
    def __init__(self, data_dir):
        csv_files = glob.glob(data_dir + "/*dnn_pred.csv")
        df_list = [pd.read_csv(file) for file in csv_files]
        zone_list = [os.path.basename(i).split('.')[0] for i in csv_files]
        self.zones = zone_list
        df_dic = {zone_list[i] : df_list[i] for i in range(len(df_list))}
        for i in df_dic:
            df_dic[i]['Date'] = pd.to_datetime(df_dic[i]['datetime'], format='%Y-%m-%d %H')
            df_dic[i] = df_dic[i][['carbon_per_MWh','Date']]
        self.data=df_dic
       

    def get_zones(self):
        return self.zones

    def get_prediction_span(self, zone_name,datetime_start,datetime_end):
        timezone = pytz.timezone('UTC')
        return self.data[zone_name].loc[(self.data[zone_name]['Date']>=datetime_start) & (self.data[zone_name]['Date']<=datetime_end)]['carbon_per_MWh'].values
    def get_prediction(self, zone_name,datetime):
        timezone = pytz.timezone('UTC')
        return self.data[zone_name].loc[self.data[zone_name]['Date']==timezone.localize(datetime)]['carbon_per_MWh'].values[0]


