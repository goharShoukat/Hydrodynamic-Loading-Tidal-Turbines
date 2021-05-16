#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 12:50:55 2021

@author: goharshoukat
"""

import pandas as pd
import numpy as np
import os
path_data_files = 'essais_ifremer_04_2021/LDV/2021_04_hydrol_ECN/'
#load the names of the files in the ldv folder to rename
files = (os.listdir(path_data_files))
files = np.sort(files)[2:]

#change path to read the new file names
renamed_files_strain_gauges = 'essais_ifremer_04_2021/'
df = pd.read_csv(renamed_files_strain_gauges + 'Data_File_Summary.csv')
df2= df.sort_values(by = 'Original')
df2 = df2.reset_index(drop = True)

#array of indices to drop from the dataframe
drop_index = np.arange(167,184,1)
df2 = df2.drop(drop_index)
df2 = df2.drop(77) #ldv does not contain this run
df2 = df2.reset_index(drop=True) #reindex after deleting that
#create new folder to move the renamed files
target_path_data_files = 'essais_ifremer_04_2021/LDV/2021_04_hydrol_ECN/renamed/'


try: os.mkdir(target_path_data_files)
except: pass

#create an array to append the new names to which will be added as a column to the data frame 
new_name = []
#run a loop to rename each file
for file in files:
    if file == 'renamed':
        pass
    else:
        #assign variable name the renamed string from column new. strip the first 3 characters THE
        #replace the first 3 characters with LDV
        name = df2[df2['Original']==file[:-11]]['New'].iloc[0][3:]
        name = 'LDV' + name
        new_name = np.append(new_name, name)
        
        #rename files
        os.rename(path_data_files + file, target_path_data_files + name + '.txt')
#create a new dataframe with the original and new names
df3 = pd.DataFrame({'Original':df2['Original'], 'LDV File Name':new_name})
new_df = pd.merge(df, df3, on = 'Original', how = 'left')
        
new_df = new_df.drop(columns={'Unnamed: 0'})
new_df = new_df.rename(columns = {'New':'Force File Name'})
new_df.to_csv('essais_ifremer_04_2021/Data_File_Summary_V2.csv')
