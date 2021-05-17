#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:25:58 2021

@author: goharshoukat
"""

import numpy as np
import pandas as pd
import os
from load_ldv3D import load_ldv3D
from data_import_func import access_file

general_path = 'essais_ifremer_04_2021/'
path_ldv_files = general_path + 'LDV/2021_04_hydrol_ECN/renamed/' 
path_data_files = general_path +  '2021_04_hydrol_ECN/'

#dfs = data file summary containing all names and flow parameters
dfs = pd.read_csv(general_path + 'Data_File_Summary_V2.csv')
ldv_files = np.array(os.listdir(path_ldv_files)) #load the file names in the ldv folder
force_files = np.sort(os.listdir(path_data_files))[2:169] #sorting + deletion of extra files


#first create a velocity data frame with only the details of the files
vel_df= pd.DataFrame({'Original Name':dfs['Original'],'LDV Name':dfs['LDV File Name'], 'U_mean' : None, 'U^2_mean':None, 'U^3_mean':None})


#add the U**2 and U**3 columns to this DF
for file in ldv_files:
    t, u = load_ldv3D(path_ldv_files+file, 0)
    u2 = np.mean(u**2)
    u3 = np.mean(u**3)
    u = np.mean(u)
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U_mean'] = u
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U^2_mean'] = u2
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U^3_mean'] = u3
    
    
#creaet a data frame with average of the thrust and RPM from the data files
force_df = pd.DataFrame({'Original Name':dfs['Original'], 'Force Name':dfs['Force File Name'], 'RPM' : None, 'Thrust_mean' : None, 'Torque_mean' : None})
for file in force_files:
    #reading the entire data file can slow down the process
    #in future, this functionality can be adjusted
    #units are being returned as well which we will be dumping
    df, _ = access_file(path_data_files + file)
    rpm_mean = np.mean(df['RPM']) 
    thrust_mean = np.mean(df['Force'])
    torque_mean = np.mean(df['Couple'])
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'RPM'] = rpm_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Thrust_mean'] = thrust_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Torque_mean'] = torque_mean

#plot Cp curve
#Eq: Cp = Torque x RPM / 0.5 x rho x A x u^3_mean
vel_df = vel_df.rename(columns = {'Original Name':'Original'})
dfs = pd.merge(dfs, vel_df, on = 'Original', how = 'left')
