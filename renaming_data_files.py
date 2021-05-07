#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:14:19 2021

@author: goharshoukat
"""

import pandas as pd
import numpy as np
import os

path_data_files = 'essais_ifremer_04_2021/2021_04_hydrol_ECN/'
path_flow_para = 'essais_ifremer_04_2021/'
target_path_data_files = 'essais_ifremer_04_2021_renamed/'
#read the excel file as a dataframe containing flow parameters
df_original = pd.read_csv(path_flow_para+'Flow_Parameters.csv', sep=';')
df_original = df_original.drop(columns='Unnamed: 6')
df = df_original.sort_values(by = 'Name')
#remove the commas from the columns
df.replace(',','', regex=True, inplace=True)
df['Reletive Position'] = df['Reletive Position'].str.replace('000','')
df['TSR'] = df['TSR'].str[:2]
#load all filenames within the folder
files = (os.listdir(path_data_files))
#sort and drop the unnecessary file names. 
files = np.sort(files)
files = files[4:-17]
df['Velocity'] = df['Velocity'].replace('1', '10')
#reindexing after sorting
df = df.reset_index(drop=True)
#array of indices to drop from the dataframe
drop_index = np.arange(167,184,1)
df = df.drop(drop_index)
#fill nan position with position N for No Mast
df['Reletive Position'] = df['Reletive Position'].fillna('XXX')


# %%
#short run or long run information not in excel sheet. each file will be
#individually opened and then closed to save memory. 
#an array with S or L will be made for this. 
    
time = []
#time data is in line 2, however, for the enumerate function to work, array 
#needs to be provided. 
lines_to_read = np.arange(2,3,1)

for file in files:
    file_path = os.path.join(path_data_files, file)
    a_file = open(file_path)

    for position, line in enumerate(a_file):
         if position in lines_to_read:
             if line[-9:-5] == ' 360.':
                 line[-9:-5] = '360'
             time.append(line[-9:-5])
time = np.array(list(map(int, time)))
l_s = time > 360
df['Time'] = l_s
df['Time'] = df['Time'].map({True:'L', False: 'S'})
# %%
try: os.mkdir(target_path_data_files)
except: pass

new_name = []
#create the new file name, read the corresponding information from the dataframe
#and then rename. the original files are renamed here. A backup is maintained
for file in files:
    #condition established to ensure length of characters remains the same. 
    if df[df['Name']==file[:-4]]['Reletive Position'].iloc[0] == '93':
        
        name = 'THE0421V' + df[df['Name']==file[:-4]]['Velocity'].iloc[0] + \
        'TSR' + df[df['Name']==file[:-4]]['TSR'].iloc[0] + \
        'P0' + df[df['Name']==file[:-4]]['Reletive Position'].iloc[0] + \
        df[df['Name']==file[:-4]]['Time'].iloc[0] + 'R1'
    else:
        name = 'THE0421V' + df[df['Name']==file[:-4]]['Velocity'].iloc[0] + \
        'TSR' + df[df['Name']==file[:-4]]['TSR'].iloc[0] + \
        'P' + df[df['Name']==file[:-4]]['Reletive Position'].iloc[0] + \
        df[df['Name']==file[:-4]]['Time'].iloc[0] + 'R1'        
    
    new_name = np.append(new_name, name)
        
    os.rename(path_data_files+file, target_path_data_files + name + '.txt')

#create a column in the original data frame read from the csv with the new names    
df_original = df_original.rename(columns={'Name':'Original'})

#a new dataframe is created which houses the old and new names to join to the original dataframe
name_frame = pd.DataFrame()
name_frame['Original'] = files
name_frame['New'] = new_name
name_frame['Original'] = name_frame['Original'].str.replace('.txt','')
#join the two dataframes together
new_df = pd.merge(df_original, name_frame, on = 'Original', how='left')

#write the new dataframe with the names and the upto date information
new_df.to_csv(path_flow_para + 'Data_File_Summary.csv')
        

