import pandas as pd
import numpy as np
import glob
import os

def get_data_and_state_list(pwd='.'):
    # Get CSV files list from a folder
    path = pwd + '/data/USA'
    csv_files = glob.glob(path + "/*.csv")

    # Read each CSV file into DataFrame
    # This creates a list of dataframes
    df_list = [pd.read_csv(file) for file in csv_files]
    state_list = [os.path.basename(i).split('.')[0] for i in csv_files]
    
    return df_list, state_list
    

def load_train_test_data(pwd='.', return_classes=True):
    df_list, state_list = get_data_and_state_list(pwd)
    df_dic = {state_list[i] : df_list[i] for i in range(len(df_list))}
    
    #Drop unnecessary columns and covert data
    for i in df_dic:
        df_dic[i]['Date'] = pd.to_datetime(df_dic[i]['datetime'], format='%Y-%m-%d %H')
        df_dic[i] = df_dic[i][['carbon_per_MWh','Date']]
        
    #Prepare data for train/test split
    for i in df_dic:
        df_dic[i].index = df_dic[i]['Date']
        del df_dic[i]['Date']
        
    train_list = []
    test_list = []
    for i in df_dic:
        train_list.append(df_dic[i][df_dic[i].index <= pd.to_datetime("2021-12-31 00:00:00+00:00", format='%Y-%m-%d %H')])
        test_list.append(df_dic[i][df_dic[i].index > pd.to_datetime("2021-12-31 00:00:00+00:00", format='%Y-%m-%d %H')])
    
    if return_classes:
        return (train_list, test_list) , state_list
    else:
        return train_list, test_list
        

def get_data_and_country_list(pwd='.'):
    # Get CSV files list from a folder
    path = pwd + '/data/europe'
    csv_files = glob.glob(path + "/*.csv")

    # Read each CSV file into DataFrame
    # This creates a list of dataframes
    df_list = [pd.read_csv(file) for file in csv_files]
    country_list = [os.path.basename(i).split('.')[0] for i in csv_files]
    
    return df_list, country_list
    

def load_train_test_data_eu(pwd='.', return_classes=True):
    df_list, country_list = get_data_and_country_list(pwd)
    df_dic = {country_list[i] : df_list[i] for i in range(len(df_list))}
    
    #Drop unnecessary columns and covert data
    for i in df_dic:
        df_dic[i]['Date'] = pd.to_datetime(df_dic[i]['datetime'], format='%Y-%m-%d %H')
        df_dic[i] = df_dic[i][['carbon_per_MWh','Date']]
        
    #Prepare data for train/test split
    for i in df_dic:
        df_dic[i].index = df_dic[i]['Date']
        del df_dic[i]['Date']
        
    train_list = []
    test_list = []
    for i in df_dic:
        train_list.append(df_dic[i][df_dic[i].index <= pd.to_datetime("2021-12-31 00:00:00+00:00", format='%Y-%m-%d %H')])
        test_list.append(df_dic[i][df_dic[i].index > pd.to_datetime("2021-12-31 00:00:00+00:00", format='%Y-%m-%d %H')])
    
    if return_classes:
        return (train_list, test_list) , country_list
    else:
        return train_list, test_list

