#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:25:58 2021

@author: goharshoukat
"""

import numpy as np
import pandas as pd
import os
from Dashboard.load_ldv3D import load_ldv3D
from Dashboard.data_import_func import access_file
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
#add standard deviation as well to study the results
vel_df= pd.DataFrame({'Original Name':dfs['Original'],'LDV Name':dfs['LDV File Name'], \
                      'U_mean' : None, 'U^2_mean' : None, 'U^3_mean' : None, \
                    'Sigma_U': None, 'Sigma_U^2' : None, 'Sigma_U^3' : None})
#add the U**2 and U**3 columns to this DF
#these are the measured values. The velocity recorded by the ldv incident on the turbine fluctuates. 
for file in ldv_files:
    t, u = load_ldv3D(path_ldv_files+file, 0)
    u2 = np.mean(u**2)
    u3 = np.mean(u**3)
    ubar = np.mean(u)
    sigmaU = np.std(u)
    sigmaU2 = np.std(u**2)
    sigmaU3 = np.std(u**3)
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U_mean'] = ubar
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U^2_mean'] = u2
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'U^3_mean'] = u3
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'Sigma_U'] = sigmaU
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'Sigma_U^2'] = sigmaU2
    vel_df.at[vel_df[vel_df['LDV Name']==file[:-4]].index[0], 'Sigma_U^3'] = sigmaU3
    
#rename columns to match the original data file
vel_df = vel_df.rename(columns = {'Original Name':'Original', 'LDV Name':'LDV File Name'})
#merge the velocity columns
dfs = pd.merge(dfs, vel_df[['Original', 'U_mean', 'U^2_mean', 'U^3_mean', 'Sigma_U', 'Sigma_U^2', 'Sigma_U^3']], on = 'Original', how = 'left')

#creaet a data frame with average of the thrust and RPM from the data files
force_df = pd.DataFrame({'Original Name':dfs['Original'], 'Force Name':dfs['Force File Name'], \
                         'RPM' : None, 'Thrust_mean' : None, 'Torque_mean' : None, \
                        'Thrust sigma' : None, 'Torque sigma' : None, 'Cp mean' : None, \
                            'Cp sigma' : None, 'Ct mean' : None, 'Ct sigma' : None, 'My1 Mean' : None, 'My1 sigma' : None})

#Cp curve
#Eq: Cp = Torque x RPM / 0.5 x rho x A x u^3_mean
rho = 1000 #water density in kg/m3
rotor_dia = 0.724
rotor_area = math.pi * rotor_dia**2 / 4
for file in force_files:
    #reading the entire data file can slow down the process
    #in future, this functionality can be adjusted
    #units are being returned as well which we will be dumping
    df, _ = access_file(path_data_files + file)
    rpm_mean = np.mean(df['RPM']) 
    thrust_mean = np.mean(df['Force'])
    torque_mean = np.mean(df['Couple'])
    thrust_std = np.std(df['Force'])
    torque_std  = np.std(df['Couple'])
    My1_mean = np.mean(df['My1'])
    My1_std = np.std(df['My1'])
    My2_mean = np.mean(df['My2'])
    My2_std = np.std(df['My2'])
    My3_mean = np.mean(df['My3'])
    My3_std = np.std(df['My3'])
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'RPM'] = rpm_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Thrust_mean'] = thrust_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Torque_mean'] = torque_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Torque sigma'] = torque_std
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Thrust sigma'] = thrust_std
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My1 sigma'] = My1_std
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My1 mean'] = My1_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My2 sigma'] = My2_std
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My2 mean'] = My2_mean
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My3 sigma'] = My3_std
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'My3 mean'] = My3_mean
    
    
    
    #calculate instantenous Cp and Ct
    Cp =  df['Couple'] * df['RPM'] * 2 * np.pi/60 / float(0.5 * rho * \
                                                rotor_area * dfs[dfs['Force File Name'] == file[:-4]]['U^3_mean'])
    Ct = df['Force'] / float(0.5 * rho * rotor_area * dfs[dfs['Force File Name'] == file[:-4]]['U^2_mean'])
    
    
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Cp mean'] = np.mean(Cp)
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Cp sigma'] = np.std(Cp)
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Ct mean'] = np.mean(Ct)
    force_df.at[force_df[force_df['Force Name']==file[:-4]].index[0], 'Ct sigma'] = np.std(Ct)
    


#rename columns to match the original data file
force_df = force_df.rename(columns = {'Original Name':'Original'})
#merge the velocity columns
dfs = pd.merge(dfs, force_df[['Original', 'RPM', 'Thrust_mean', 'Torque_mean', 'Torque sigma', 'Thrust sigma', 'Cp mean', 'Cp sigma', 'Ct mean', 'Ct sigma', 'My1 mean', 'My1 sigma','My2 mean', 'My2 sigma','My3 mean', 'My3 sigma']], on = 'Original', how = 'left')

dfs.to_csv('Cp_Ct/Experiment_Summary.csv')

#create seperate dataframes depending on the positions
#the below calculation can take place through simple function. 
#some files are missing however which complicate the matter
#perhaps in the future, a comprehensive function can do thejob
# %% DataFrame for Position = Sans Mat
path_performance_curves = 'Results/Performance Coefficients/Position Focus/'
#velocity 0.8 m/s
pxxxv08 = dfs.fillna('xxx')
pxxxv08['TSR'] = pxxxv08['TSR'].str.replace(',','.')
pxxxv08 = pxxxv08[(pxxxv08['Force File Name'].str.contains(r'PXXX')) & (pxxxv08['Velocity']=='0,8')]
#Cp_errorxxxv08 = [pxxxv08['Cp mean'] - pxxxv08['Cp sigma'], pxxxv08['Cp mean'] - pxxxv08['Cp sigma']]
#Ct_errorxxxv08 = [pxxxv08['Ct mean'] - pxxxv08['Ct sigma'], pxxxv08['Ct mean'] - pxxxv08['Ct sigma']]
Cp_errorxxxv08 = pxxxv08['Cp sigma']
Ct_errorxxxv08 = pxxxv08['Ct sigma']


#velocity 1 m/s
pxxxv10 = dfs.fillna('xxx')
pxxxv10['TSR'] = pxxxv10['TSR'].str.replace(',','.')
pxxxv10 = pxxxv10[(pxxxv10['Force File Name'].str.contains(r'PXXX')) & (pxxxv10['Velocity']=='1')].drop(183) #drop the 183rd index which is the long run
#Cp_errorxxxv10 = [pxxxv10['Cp mean'] - pxxxv10['Cp sigma'], pxxxv10['Cp mean'] - pxxxv10['Cp sigma']]
#Ct_errorxxxv10 = [pxxxv10['Ct mean'] - pxxxv10['Ct sigma'], pxxxv10['Ct mean'] - pxxxv10['Ct sigma']]
Cp_errorxxxv10 = pxxxv10['Cp sigma']
Ct_errorxxxv10 = pxxxv10['Ct sigma']


#velocity 1.2 m/s
pxxxv12 = dfs.fillna('xxx')
pxxxv12['TSR'] = pxxxv12['TSR'].str.replace(',','.')
pxxxv12 = pxxxv12[(pxxxv12['Force File Name'].str.contains(r'PXXX')) & (pxxxv12['Velocity']=='1,2')]
#Cp_errorxxxv12 = [pxxxv12['Cp mean'] - pxxxv12['Cp sigma'], pxxxv12['Cp mean'] - pxxxv12['Cp sigma']]
#Ct_errorxxxv12 = [pxxxv12['Ct mean'] - pxxxv12['Ct sigma'], pxxxv12['Ct mean'] - pxxxv12['Ct sigma']]
Cp_errorxxxv12 = pxxxv12['Cp sigma']
Ct_errorxxxv12 =  pxxxv12['Ct sigma']



#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar((pxxxv08['TSR'].astype(float)),(pxxxv08['Cp mean'].astype(float)), yerr= Cp_errorxxxv08, label = 'Velocity = 0.8 m/s')
plt.errorbar((pxxxv10['TSR'].astype(float)),(pxxxv10['Cp mean'].astype(float)), yerr= Cp_errorxxxv10, label = 'Velocity = 1.0 m/s')
plt.errorbar((pxxxv12['TSR'].astype(float)),(pxxxv12['Cp mean'].astype(float)), yerr= Cp_errorxxxv12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p PXXX.png')
plt.close()

#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.errorbar((pxxxv08['TSR'].astype(float)),(pxxxv08['Ct mean'].astype(float)), yerr= Ct_errorxxxv08, label = 'Velocity = 0.8 m/s')
plt.errorbar((pxxxv10['TSR'].astype(float)),(pxxxv10['Ct mean'].astype(float)), yerr= Ct_errorxxxv10, label = 'Velocity = 1.0 m/s')
plt.errorbar((pxxxv12['TSR'].astype(float)),(pxxxv12['Ct mean'].astype(float)), yerr= Ct_errorxxxv12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t PXXX.png')
plt.close()
# %% DataFrame for Position = 594mm
#velocity 0.8 m/s
p594v08 = dfs.fillna('xxx')
p594v08['TSR'] = p594v08['TSR'].str.replace(',','.')
p594v08 = p594v08[(p594v08['Force File Name'].str.contains(r'P594')) & (p594v08['Velocity']=='0,8')]
Cp_error594v08 = p594v08['Cp sigma']
Ct_error594v08 = p594v08['Ct sigma']

#velocity 1 m/s
p594v10 = dfs.fillna('594')
p594v10['TSR'] = p594v10['TSR'].str.replace(',','.')
p594v10 = p594v10[(p594v10['Force File Name'].str.contains(r'P594')) & (p594v10['Velocity']=='1')] #drop the 183rd index which is the long run
Cp_error594v10 = p594v10['Cp sigma']
Ct_error594v10 = p594v10['Ct sigma']
#velocity 1.2 m/s
p594v12 = dfs.fillna('594')
p594v12['TSR'] = p594v12['TSR'].str.replace(',','.')
p594v12 = p594v12[(p594v12['Force File Name'].str.contains(r'P594')) & (p594v12['Velocity']=='1,2')]
Cp_error594v12 = p594v12['Cp sigma']
Ct_error594v12 = p594v12['Ct sigma']

plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar((p594v08['TSR'].astype(float)),(p594v08['Cp mean'].astype(float)), yerr= Cp_error594v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p594v10['TSR'].astype(float)),(p594v10['Cp mean'].astype(float)), yerr= Cp_error594v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p594v12['TSR'].astype(float)),(p594v12['Cp mean'].astype(float)), yerr= Cp_error594v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P594.png')
plt.close()

#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.errorbar((p594v08['TSR'].astype(float)),(p594v08['Ct mean'].astype(float)), yerr= Ct_error594v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p594v10['TSR'].astype(float)),(p594v10['Ct mean'].astype(float)), yerr= Ct_error594v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p594v12['TSR'].astype(float)),(p594v12['Ct mean'].astype(float)), yerr= Ct_error594v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P594.png')
plt.close()
# %% DataFrame for Position = 427mm
#velocity 0.8 m/s
p427v08 = dfs.fillna('xxx')
p427v08['TSR'] = p427v08['TSR'].str.replace(',','.')
p427v08 = p427v08[(p427v08['Force File Name'].str.contains(r'P427')) & (p427v08['Velocity']=='0,8')].drop(85) #missing ldv file for run78. hence dropped
Cp_error427v08 = p427v08['Cp sigma']
Ct_error427v08 = p427v08['Ct sigma']

#velocity 1 m/s
p427v10 = dfs.fillna('427')
p427v10['TSR'] = p427v10['TSR'].str.replace(',','.')
p427v10 = p427v10[(p427v10['Force File Name'].str.contains(r'P427')) & (p427v10['Velocity']=='1')] #drop the 183rd index which is the long run
Cp_error427v10 = p427v10['Cp sigma']
Ct_error427v10 = p427v10['Ct sigma']

#velocity 1.2 m/s
p427v12 = dfs.fillna('427')
p427v12['TSR'] = p427v12['TSR'].str.replace(',','.')
p427v12 = p427v12[(p427v12['Force File Name'].str.contains(r'P427')) & (p427v12['Velocity']=='1,2')]
Cp_error427v12 = p427v12['Cp sigma']
Ct_error427v12 = p427v12['Ct sigma']

plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar((p427v08['TSR'].astype(float)),(p427v08['Cp mean'].astype(float)), yerr= Cp_error427v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p427v10['TSR'].astype(float)),(p427v10['Cp mean'].astype(float)), yerr= Cp_error427v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p427v12['TSR'].astype(float)),(p427v12['Cp mean'].astype(float)), yerr= Cp_error427v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P427.png')
plt.close()

#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.errorbar((p427v08['TSR'].astype(float)),(p427v08['Ct mean'].astype(float)), yerr= Ct_error427v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p427v10['TSR'].astype(float)),(p427v10['Ct mean'].astype(float)), yerr= Ct_error427v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p427v12['TSR'].astype(float)),(p427v12['Ct mean'].astype(float)), yerr= Ct_error427v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P427.png')
plt.close()
# %% DataFrame for Position = 260 mm
#velocity 0.8 m/s
p260v08 = dfs.fillna('xxx')
p260v08['TSR'] = p260v08['TSR'].str.replace(',','.')
p260v08 = p260v08[(p260v08['Force File Name'].str.contains(r'P260')) & (p260v08['Velocity']=='0,8')]
Cp_error260v08 = p260v08['Cp sigma']
Ct_error260v08 = p260v08['Ct sigma']
#velocity 1 m/s
p260v10 = dfs.fillna('260')
p260v10['TSR'] = p260v10['TSR'].str.replace(',','.')
p260v10 = p260v10[(p260v10['Force File Name'].str.contains(r'P260')) & (p260v10['Velocity']=='1')].drop(123) #drop the 183rd index which is the long run
Cp_error260v10 = p260v10['Cp sigma']
Ct_error260v10 = p260v10['Ct sigma']
    
#velocity 1.2 m/s
#for this position, this velocity was not used
#p260v12 = dfs.fillna('260')
#p260v12['TSR'] = p260v12['TSR'].str.replace(',','.')
#p260v12 = p260v12[(p260v12['Force File Name'].str.contains(r'P260')) & (p260v12['Velocity']=='1,2')]


#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar((p260v08['TSR'].astype(float)),(p260v08['Cp mean'].astype(float)), yerr= Cp_error260v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p260v10['TSR'].astype(float)),(p260v10['Cp mean'].astype(float)), yerr= Cp_error260v10, label = 'Velocity = 1.0 m/s')
#plt.errorbar((p260v12['TSR'].astype(float)),(p260v12['Cp mean'].astype(float)), yerr= Cp_error260v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P260.png')
plt.close()

#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.errorbar((p260v08['TSR'].astype(float)),(p260v08['Ct mean'].astype(float)), yerr= Ct_error260v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p260v10['TSR'].astype(float)),(p260v10['Ct mean'].astype(float)), yerr= Ct_error260v10, label = 'Velocity = 1.0 m/s')
#plt.errorbar((p260v12['TSR'].astype(float)),(p260v12['Ct mean'].astype(float)), yerr= Ct_error260v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P260.png')
plt.close()
# %% DataFrame for Position = 93 mm
#velocity 0.8 m/s
p093v08 = dfs.fillna('xxx')
p093v08['TSR'] = p093v08['TSR'].str.replace(',','.')
p093v08 = p093v08[(p093v08['Force File Name'].str.contains(r'P093')) & (p093v08['Velocity']=='0,8')]
Cp_error093v08 = p093v08['Cp sigma']
Ct_error093v08 = p093v08['Ct sigma']
#velocity 1 m/s
p093v10 = dfs.fillna('093')
p093v10['TSR'] = p093v10['TSR'].str.replace(',','.')
p093v10 = p093v10[(p093v10['Force File Name'].str.contains(r'P093')) & (p093v10['Velocity']=='1')].drop(73) #long run is dropped
Cp_error093v10 = p093v10['Cp sigma']
Ct_error093v10 = p093v10['Ct sigma']
#velocity 1.2 m/s
#for this position, this velocity was not used
p093v12 = dfs.fillna('093')
p093v12['TSR'] = p093v12['TSR'].str.replace(',','.')
p093v12 = p093v12[(p093v12['Force File Name'].str.contains(r'P093')) & (p093v12['Velocity']=='1,2')]
Cp_error093v12 = p093v10['Cp sigma']
Ct_error093v12 = p093v10['Ct sigma']

#plot and save Cp
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar((p093v08['TSR'].astype(float)),(p093v08['Cp mean'].astype(float)), yerr= Cp_error093v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p093v10['TSR'].astype(float)),(p093v10['Cp mean'].astype(float)), yerr= Cp_error093v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p093v12['TSR'].astype(float)),(p093v12['Cp mean'].astype(float)), yerr= Cp_error093v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p P093.png')
plt.close()

#plot and save Ct
plt.xlabel('TSR')
plt.ylabel('$C_T$')
plt.errorbar((p093v08['TSR'].astype(float)),(p093v08['Ct mean'].astype(float)), yerr= Ct_error093v08, label = 'Velocity = 0.8 m/s')
plt.errorbar((p093v10['TSR'].astype(float)),(p093v10['Ct mean'].astype(float)), yerr= Ct_error093v10, label = 'Velocity = 1.0 m/s')
plt.errorbar((p093v12['TSR'].astype(float)),(p093v12['Ct mean'].astype(float)), yerr= Ct_error093v12, label = 'Velocity = 1.2 m/s')
plt.legend(loc = 'lower right')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t P093.png')
plt.close()

# %% read the csv including the indication for error files
dfs2 = pd.read_csv('Cp_Ct/Experiment_Summary.csv')
#dfs2['Error_File'] = dfs2['Error_File'].str.replace(',00','')

# %% Plotting graphs with focus on positions
path_performance_curves = 'Results/Performance Coefficients/Velocity Focus/'
v08 = dfs2.fillna('xxx')
v08['TSR'] = v08['TSR'].str.replace(',','.')
v08 = (v08[v08['Velocity']=='0,8'].drop(85))
Cpv08Pxxx = v08[v08['Reletive Position'] == 'xxx']['Cp sigma']
Cpv08P594 = v08[v08['Reletive Position'] == '594,000']['Cp sigma']
Cpv08P427 = v08[v08['Reletive Position'] == '427,000']['Cp sigma']
Cpv08P260 = v08[v08['Reletive Position'] == '260,000']['Cp sigma']
Cpv08P093 = v08[v08['Reletive Position'] == '93,000']['Cp sigma']
Ctv08Pxxx = v08[v08['Reletive Position'] == 'xxx']['Cp sigma']
Ctv08P594 = v08[v08['Reletive Position'] == '594,000']['Ct sigma']
Ctv08P427 = v08[v08['Reletive Position'] == '427,000']['Ct sigma']
Ctv08P260 = v08[v08['Reletive Position'] == '260,000']['Ct sigma']
Ctv08P093 = v08[v08['Reletive Position'] == '93,000']['Ct sigma']

#plot and save Cp for velocity of v=0.8m/s
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar(v08[v08['Reletive Position']=='xxx']['TSR'].astype(float), v08[v08['Reletive Position']=='xxx']['Cp mean'].astype(float), yerr = Cpv08Pxxx,label = 'Without Mast')
plt.errorbar(v08[v08['Reletive Position']=='594,000']['TSR'].astype(float), v08[v08['Reletive Position']=='594,000']['Cp mean'].astype(float), yerr = Cpv08P594, label = '594 mm')
plt.errorbar(v08[v08['Reletive Position']=='427,000']['TSR'].astype(float), v08[v08['Reletive Position']=='427,000']['Cp mean'].astype(float), yerr = Cpv08P427, label = '427 mm')
plt.errorbar(v08[v08['Reletive Position']=='260,000']['TSR'].astype(float), v08[v08['Reletive Position']=='260,000']['Cp mean'].astype(float), yerr = Cpv08P260, label = '260 mm')
plt.errorbar(v08[v08['Reletive Position']=='93,000']['TSR'].astype(float), v08[v08['Reletive Position']=='93,000']['Cp mean'].astype(float), yerr = Cpv08P093, label = '93 mm')
#plt.plot(v08[v08['Reletive Position']=='93,000']['TSR'].astype(float), v08[v08['Reletive Position']=='93,000']['Cp mean'].astype(float), label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p V0.8.png')
plt.close()
#plot and save Cp for velocity of v=0.8m/s
plt.xlabel('TSR')
plt.ylabel('$C_t$')
plt.errorbar(v08[v08['Reletive Position']=='xxx']['TSR'].astype(float), v08[v08['Reletive Position']=='xxx']['Ct mean'].astype(float), yerr = Ctv08Pxxx, label = 'Without Mast')
plt.errorbar(v08[v08['Reletive Position']=='594,000']['TSR'].astype(float), v08[v08['Reletive Position']=='594,000']['Ct mean'].astype(float), yerr = Ctv08P594, label = '594 mm')
plt.errorbar(v08[v08['Reletive Position']=='427,000']['TSR'].astype(float), v08[v08['Reletive Position']=='427,000']['Ct mean'].astype(float), yerr = Ctv08P427, label = '427 mm')
plt.errorbar(v08[v08['Reletive Position']=='260,000']['TSR'].astype(float), v08[v08['Reletive Position']=='260,000']['Ct mean'].astype(float), yerr = Ctv08P260, label = '260 mm')
plt.errorbar(v08[v08['Reletive Position']=='93,000']['TSR'].astype(float), v08[v08['Reletive Position']=='93,000']['Ct mean'].astype(float), yerr = Ctv08P093, label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t V0.8.png')
plt.close()
# %% Velocity 1.0 m/s
v10 = dfs2.fillna('xxx')
v10['TSR'] = v10['TSR'].str.replace(',','.')
#drop the rows without TSR sweep information and longrun 
v10 = v10[v10['Velocity']=='1'].drop(np.arange(160, 170, 1)).drop([73, 123, 183])
Cpv10Pxxx = v10[v10['Reletive Position'] == 'xxx']['Cp sigma']
Cpv10P594 = v10[v10['Reletive Position'] == '594,000']['Cp sigma']
Cpv10P427 = v10[v10['Reletive Position'] == '427,000']['Cp sigma']
Cpv10P260 = v10[v10['Reletive Position'] == '260,000']['Cp sigma']
Cpv10P093 = v10[v10['Reletive Position'] == '93,000']['Cp sigma']
Ctv10Pxxx = v10[v10['Reletive Position'] == 'xxx']['Cp sigma']
Ctv10P594 = v10[v10['Reletive Position'] == '594,000']['Ct sigma']
Ctv10P427 = v10[v10['Reletive Position'] == '427,000']['Ct sigma']
Ctv10P260 = v10[v10['Reletive Position'] == '260,000']['Ct sigma']
Ctv10P093 = v10[v10['Reletive Position'] == '93,000']['Ct sigma']

#plot and save Cp for velocity of v=0.8m/s
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar(v10[v10['Reletive Position']=='xxx']['TSR'].astype(float), v10[v10['Reletive Position']=='xxx']['Cp mean'].astype(float), yerr = Cpv10Pxxx,label = 'Without Mast')
plt.errorbar(v10[v10['Reletive Position']=='594,000']['TSR'].astype(float), v10[v10['Reletive Position']=='594,000']['Cp mean'].astype(float), yerr = Cpv10P594, label = '594 mm')
plt.errorbar(v10[v10['Reletive Position']=='427,000']['TSR'].astype(float), v10[v10['Reletive Position']=='427,000']['Cp mean'].astype(float), yerr = Cpv10P427, label = '427 mm')
plt.errorbar(v10[v10['Reletive Position']=='260,000']['TSR'].astype(float), v10[v10['Reletive Position']=='260,000']['Cp mean'].astype(float), yerr = Cpv10P260, label = '260 mm')
plt.errorbar(v10[v10['Reletive Position']=='93,000']['TSR'].astype(float), v10[v10['Reletive Position']=='93,000']['Cp mean'].astype(float), yerr = Cpv10P093, label = '93 mm')
#plt.plot(v10[v10['Reletive Position']=='93,000']['TSR'].astype(float), v10[v10['Reletive Position']=='93,000']['Cp mean'].astype(float), label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p V1.0.png')
plt.close()
#plot and save Cp for velocity of v=1.0m/s
plt.xlabel('TSR')
plt.ylabel('$C_t$')
plt.errorbar(v10[v10['Reletive Position']=='xxx']['TSR'].astype(float), v10[v10['Reletive Position']=='xxx']['Ct mean'].astype(float), yerr = Ctv10Pxxx, label = 'Without Mast')
plt.errorbar(v10[v10['Reletive Position']=='594,000']['TSR'].astype(float), v10[v10['Reletive Position']=='594,000']['Ct mean'].astype(float), yerr = Ctv10P594, label = '594 mm')
plt.errorbar(v10[v10['Reletive Position']=='427,000']['TSR'].astype(float), v10[v10['Reletive Position']=='427,000']['Ct mean'].astype(float), yerr = Ctv10P427, label = '427 mm')
plt.errorbar(v10[v10['Reletive Position']=='260,000']['TSR'].astype(float), v10[v10['Reletive Position']=='260,000']['Ct mean'].astype(float), yerr = Ctv10P260, label = '260 mm')
plt.errorbar(v10[v10['Reletive Position']=='93,000']['TSR'].astype(float), v10[v10['Reletive Position']=='93,000']['Ct mean'].astype(float), yerr = Ctv10P093, label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t V1.0.png')
plt.close()

# %% Velocity 1.2 m/s
v12 = dfs2.fillna('xxx')
v12['TSR'] = v12['TSR'].str.replace(',','.')
#drop the rows without TSR sweep information and longrun 
v12 = v12[v12['Velocity']=='1,2']
Cpv12Pxxx = v12[v12['Reletive Position'] == 'xxx']['Cp sigma']
Cpv12P594 = v12[v12['Reletive Position'] == '594,000']['Cp sigma']
Cpv12P427 = v12[v12['Reletive Position'] == '427,000']['Cp sigma']
Cpv12P260 = v12[v12['Reletive Position'] == '260,000']['Cp sigma']
Cpv12P093 = v12[v12['Reletive Position'] == '93,000']['Cp sigma']
Ctv12Pxxx = v12[v12['Reletive Position'] == 'xxx']['Cp sigma']
Ctv12P594 = v12[v12['Reletive Position'] == '594,000']['Ct sigma']
Ctv12P427 = v12[v12['Reletive Position'] == '427,000']['Ct sigma']
Ctv12P260 = v12[v12['Reletive Position'] == '260,000']['Ct sigma']
Ctv12P093 = v12[v12['Reletive Position'] == '93,000']['Ct sigma']

#plot and save Cp for velocity of v=0.8m/s
plt.xlabel('TSR')
plt.ylabel('$C_P$')
plt.errorbar(v12[v12['Reletive Position']=='xxx']['TSR'].astype(float), v12[v12['Reletive Position']=='xxx']['Cp mean'].astype(float), yerr = Cpv12Pxxx,label = 'Without Mast')
plt.errorbar(v12[v12['Reletive Position']=='594,000']['TSR'].astype(float), v12[v12['Reletive Position']=='594,000']['Cp mean'].astype(float), yerr = Cpv12P594, label = '594 mm')
plt.errorbar(v12[v12['Reletive Position']=='427,000']['TSR'].astype(float), v12[v12['Reletive Position']=='427,000']['Cp mean'].astype(float), yerr = Cpv12P427, label = '427 mm')
plt.errorbar(v12[v12['Reletive Position']=='260,000']['TSR'].astype(float), v12[v12['Reletive Position']=='260,000']['Cp mean'].astype(float), yerr = Cpv12P260, label = '260 mm')
plt.errorbar(v12[v12['Reletive Position']=='93,000']['TSR'].astype(float), v12[v12['Reletive Position']=='93,000']['Cp mean'].astype(float), yerr = Cpv12P093, label = '93 mm')
#plt.plot(v12[v12['Reletive Position']=='93,000']['TSR'].astype(float), v12[v12['Reletive Position']=='93,000']['Cp mean'].astype(float), label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_p V1.2.png')
plt.close()
#plot and save Cp for velocity of v=1.0m/s
plt.xlabel('TSR')
plt.ylabel('$C_t$')
plt.errorbar(v12[v12['Reletive Position']=='xxx']['TSR'].astype(float), v12[v12['Reletive Position']=='xxx']['Ct mean'].astype(float), yerr = Ctv12Pxxx, label = 'Without Mast')
plt.errorbar(v12[v12['Reletive Position']=='594,000']['TSR'].astype(float), v12[v12['Reletive Position']=='594,000']['Ct mean'].astype(float), yerr = Ctv12P594, label = '594 mm')
plt.errorbar(v12[v12['Reletive Position']=='427,000']['TSR'].astype(float), v12[v12['Reletive Position']=='427,000']['Ct mean'].astype(float), yerr = Ctv12P427, label = '427 mm')
plt.errorbar(v12[v12['Reletive Position']=='260,000']['TSR'].astype(float), v12[v12['Reletive Position']=='260,000']['Ct mean'].astype(float), yerr = Ctv12P260, label = '260 mm')
plt.errorbar(v12[v12['Reletive Position']=='93,000']['TSR'].astype(float), v12[v12['Reletive Position']=='93,000']['Ct mean'].astype(float), yerr = Ctv12P093, label = '93 mm')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()
plt.savefig(path_performance_curves + 'C_t V1.2.png')
plt.close()



