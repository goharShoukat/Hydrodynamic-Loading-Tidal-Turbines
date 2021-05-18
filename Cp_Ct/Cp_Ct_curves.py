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
import math
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
import matplotlib.pyplot as plt


general_path = 'essais_ifremer_04_2021/'
path_ldv_files = general_path + 'LDV/2021_04_hydrol_ECN/renamed/' 
path_data_files = general_path +  '2021_04_hydrol_ECN/'

#dfs = data file summary containing all names and flow parameters
dfs = pd.read_csv(general_path + 'Data_File_Summary_V2.csv')
dfs = dfs.drop(columns = {'Unnamed: 0'})
ldv_files = np.array(os.listdir(path_ldv_files)) #load the file names in the ldv folder
force_files = np.sort(os.listdir(path_data_files))[2:169] #sorting + deletion of extra files


#first create a velocity data frame with only the details of the files
vel_df= pd.DataFrame({'Original Name':dfs['Original'],'LDV Name':dfs['LDV File Name'], 'U_mean' : None, 'U^2_mean':None, 'U^3_mean':None})


#add the U**2 and U**3 columns to this DF
#these are the measured values. The velocity recorded by the ldv incident on the turbine fluctuates. 
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


#rename columns to match the original data file
vel_df = vel_df.rename(columns = {'Original Name':'Original', 'LDV Name':'LDV File Name'})
force_df = force_df.rename(columns = {'Original Name':'Original'})
#merge the velocity columns
dfs = pd.merge(dfs, vel_df[['Original', 'U_mean', 'U^2_mean', 'U^3_mean']], on = 'Original', how = 'left')
dfs = pd.merge(dfs, force_df[['Original', 'RPM', 'Thrust_mean', 'Torque_mean']], on = 'Original', how = 'left')
dfs.to_csv('Cp_Ct/Experiment_Summary.csv')


#write the new csv with the average values to avoid recalculating
#Cp curve
#Eq: Cp = Torque x RPM / 0.5 x rho x A x u^3_mean
rho = 1000 #water density in kg/m3
rotor_dia = 0.724
rotor_area = math.pi * rotor_dia**2 / 4
dfs['Cp'] = dfs['Torque_mean'] * dfs['RPM'] * 2 * np.pi/60 / (0.5 * rho * \
                                                rotor_area * dfs['U^3_mean'])
#Ct calculation
# Thrust / o.5 x rho x A x U**2_mean
dfs['Ct'] = dfs['Thrust_mean']  / (0.5 * rho * rotor_area * dfs['U^2_mean'])


#create seperate dataframes depending on the positions
#the below calculation can take place through simple function. 
#some files are missing however which complicate the matter
#perhaps in the future, a comprehensive function can do thejob
# %% DataFrame for Position = Sans Mat
path_performance_curves = 'Results/Performance Coefficients/'
#velocity 0.8 m/s
pxxxv08 = dfs.fillna('xxx')
pxxxv08['TSR'] = pxxxv08['TSR'].str.replace(',','.')
pxxxv08 = pxxxv08[(pxxxv08['Force File Name'].str.contains(r'PXXX')) & (pxxxv08['Velocity']=='0,8')]


#velocity 1 m/s
pxxxv10 = dfs.fillna('xxx')
pxxxv10['TSR'] = pxxxv10['TSR'].str.replace(',','.')
pxxxv10 = pxxxv10[(pxxxv10['Force File Name'].str.contains(r'PXXX')) & (pxxxv10['Velocity']=='1')].drop(183) #drop the 183rd index which is the long run
    
#velocity 1.2 m/s
pxxxv12 = dfs.fillna('xxx')
pxxxv12['TSR'] = pxxxv12['TSR'].str.replace(',','.')
pxxxv12 = pxxxv12[(pxxxv12['Force File Name'].str.contains(r'PXXX')) & (pxxxv12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.plot((pxxxv08['TSR'].astype(float)),(pxxxv08['Cp'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((pxxxv10['TSR'].astype(float)),(pxxxv10['Cp'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((pxxxv12['TSR'].astype(float)),(pxxxv12['Cp'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p PXXX.png')


#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.plot((pxxxv08['TSR'].astype(float)),(pxxxv08['Ct'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((pxxxv10['TSR'].astype(float)),(pxxxv10['Ct'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((pxxxv12['TSR'].astype(float)),(pxxxv12['Ct'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t PXXX.png')

# %% DataFrame for Position = 594mm
#velocity 0.8 m/s
p594v08 = dfs.fillna('xxx')
p594v08['TSR'] = p594v08['TSR'].str.replace(',','.')
p594v08 = p594v08[(p594v08['Force File Name'].str.contains(r'P594')) & (p594v08['Velocity']=='0,8')]


#velocity 1 m/s
p594v10 = dfs.fillna('594')
p594v10['TSR'] = p594v10['TSR'].str.replace(',','.')
p594v10 = p594v10[(p594v10['Force File Name'].str.contains(r'P594')) & (p594v10['Velocity']=='1')] #drop the 183rd index which is the long run
    
#velocity 1.2 m/s
p594v12 = dfs.fillna('594')
p594v12['TSR'] = p594v12['TSR'].str.replace(',','.')
p594v12 = p594v12[(p594v12['Force File Name'].str.contains(r'P594')) & (p594v12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.plot((p594v08['TSR'].astype(float)),(p594v08['Cp'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p594v10['TSR'].astype(float)),(p594v10['Cp'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((p594v12['TSR'].astype(float)),(p594v12['Cp'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P594.png')


#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.plot((p594v08['TSR'].astype(float)),(p594v08['Ct'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p594v10['TSR'].astype(float)),(p594v10['Ct'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((p594v12['TSR'].astype(float)),(p594v12['Ct'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P594.png')

# %% DataFrame for Position = 427mm
#velocity 0.8 m/s
p427v08 = dfs.fillna('xxx')
p427v08['TSR'] = p427v08['TSR'].str.replace(',','.')
p427v08 = p427v08[(p427v08['Force File Name'].str.contains(r'P427')) & (p427v08['Velocity']=='0,8')].drop(85) #missing ldv file for run78. hence dropped


#velocity 1 m/s
p427v10 = dfs.fillna('427')
p427v10['TSR'] = p427v10['TSR'].str.replace(',','.')
p427v10 = p427v10[(p427v10['Force File Name'].str.contains(r'P427')) & (p427v10['Velocity']=='1')] #drop the 183rd index which is the long run
    
#velocity 1.2 m/s
p427v12 = dfs.fillna('427')
p427v12['TSR'] = p427v12['TSR'].str.replace(',','.')
p427v12 = p427v12[(p427v12['Force File Name'].str.contains(r'P427')) & (p427v12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.plot((p427v08['TSR'].astype(float)),(p427v08['Cp'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p427v10['TSR'].astype(float)),(p427v10['Cp'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((p427v12['TSR'].astype(float)),(p427v12['Cp'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P427.png')


#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.plot((p427v08['TSR'].astype(float)),(p427v08['Ct'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p427v10['TSR'].astype(float)),(p427v10['Ct'].astype(float)), label = 'Velocity = 1.0 m/s')
plt.plot((p427v12['TSR'].astype(float)),(p427v12['Ct'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P427.png')


# %% DataFrame for Position = 260 mm
#velocity 0.8 m/s
p260v08 = dfs.fillna('xxx')
p260v08['TSR'] = p260v08['TSR'].str.replace(',','.')
p260v08 = p260v08[(p260v08['Force File Name'].str.contains(r'P260')) & (p260v08['Velocity']=='0,8')]

#velocity 1 m/s
p260v10 = dfs.fillna('260')
p260v10['TSR'] = p260v10['TSR'].str.replace(',','.')
p260v10 = p260v10[(p260v10['Force File Name'].str.contains(r'P260')) & (p260v10['Velocity']=='1')].drop(123) #drop the 183rd index which is the long run
    
#velocity 1.2 m/s
#for this position, this velocity was not used
#p260v12 = dfs.fillna('260')
#p260v12['TSR'] = p260v12['TSR'].str.replace(',','.')
#p260v12 = p260v12[(p260v12['Force File Name'].str.contains(r'P260')) & (p260v12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.plot((p260v08['TSR'].astype(float)),(p260v08['Cp'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p260v10['TSR'].astype(float)),(p260v10['Cp'].astype(float)), label = 'Velocity = 1.0 m/s')
#plt.plot((p260v12['TSR'].astype(float)),(p260v12['Cp'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P260.png')


#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.plot((p260v08['TSR'].astype(float)),(p260v08['Ct'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p260v10['TSR'].astype(float)),(p260v10['Ct'].astype(float)), label = 'Velocity = 1.0 m/s')
#plt.plot((p260v12['TSR'].astype(float)),(p260v12['Ct'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P260.png')

# %% DataFrame for Position = 93 mm
#velocity 0.8 m/s
p093v08 = dfs.fillna('xxx')
p093v08['TSR'] = p093v08['TSR'].str.replace(',','.')
p093v08 = p093v08[(p093v08['Force File Name'].str.contains(r'P093')) & (p093v08['Velocity']=='0,8')]

#velocity 1 m/s
p093v10 = dfs.fillna('093')
p093v10['TSR'] = p093v10['TSR'].str.replace(',','.')
p093v10 = p093v10[(p093v10['Force File Name'].str.contains(r'P093')) & (p093v10['Velocity']=='1')].drop(73) #long run is dropped
#velocity 1.2 m/s
#for this position, this velocity was not used
p093v12 = dfs.fillna('093')
p093v12['TSR'] = p093v12['TSR'].str.replace(',','.')
p093v12 = p093v12[(p093v12['Force File Name'].str.contains(r'P093')) & (p093v12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.plot((p093v08['TSR'].astype(float)),(p093v08['Cp'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p093v10['TSR'].astype(float)),(p093v10['Cp'].astype(float)), label = 'Velocity = 1.0 m/s')
#plt.plot((p093v12['TSR'].astype(float)),(p093v12['Cp'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P093.png')


#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.plot((p093v08['TSR'].astype(float)),(p093v08['Ct'].astype(float)), label = 'Velocity = 0.8 m/s')
plt.plot((p093v10['TSR'].astype(float)),(p093v10['Ct'].astype(float)), label = 'Velocity = 1.0 m/s')
#plt.plot((p093v12['TSR'].astype(float)),(p093v12['Ct'].astype(float)), label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P093.png')