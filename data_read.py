#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:44:10 2021

@author: goharshoukat
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import fftpack
import math
import os
import pickle
import stats_lib
#%%
'''
File Read into script
Data Cleaning, Time Stamp Addition
Simple Statistics Calculated
Initial Plots
'''

#The data file was cleaned to remove the first couple of lines. 
path = 'Prior_Data_Papers/'
df = pd.read_csv(path+'run007.txt', sep = '\t', skiprows=9)
units = df.iloc[0]
df = df.drop([0])
#renaming first column header
df = df.rename({'#RPM': 'RPM'}, axis=1)
units['RPM'] = 'RPM'
 
#all column heads are stored to recreate proper columns
col_head = list(df.columns)
#the data series is throwing an exception that the data is not numeric
#the following for loop converts the entire dataframe to numeric which 
#can then be plotted
for i in range(len(df.columns)):
    x = pd.to_numeric(df[col_head[i]])
    df = df.drop(columns=[col_head[i]])
    df.insert(i, col_head[i], x)
    del x



#Statistics of the data
std_val = df.std(axis = 0)                    # standard deviation
mean_val = df.mean(axis = 0)                  # arithmatic mean
max_val = df.max(axis = 0)                    # max values
min_val = df.min(axis = 0)                    # min values


#df.plot(subplots = True, layout = (6,4))

#Include time stamps
sampling_freq = 256 #Hz
t_per_meas = 1/256
run_time = 360#4097# 360#seconds
no_of_meas = int(run_time / t_per_meas)
# create time arra
t = np.linspace(0, run_time, no_of_meas)
#first add column to the data framce
df['time'] = t
#rename index to time values
df = df.set_index('time')

# %% Spectral Analysis
rotor_freq = mean_val[0]/60
path_fft = 'Results/fft/'
os.makedirs(path_fft)
bins = (run_time*sampling_freq)
timestep = df.index[1]

for column in df:  
    if column == 'RPM':
        pass
    else:
        spec = stats_lib.fft(df[column].to_numpy(), sampling_freq, bins)
        frequency = np.fft.fftfreq(bins, d=timestep)
        stats_lib.fft_plot(spec, column, frequency, rotor_freq, units, path_fft)
      #  plt.loglog(frequency[0:int(bins/2)], spec)
        

    
                    
# %% Rolling Averages
#create new data frame that holds the rolling mean for each property

import stats_lib

'''
Mean
'''
df_rolling_average = pd.DataFrame()
df_rolling_average_normalised = pd.DataFrame()
value_skip = 256 #
normalization = True #parameter passed onto functions to the statistics
#calculation and plotting arguments to determine if normalisation needs to 
#be carried out. 
for column in df.columns:
    
    if normalization == True:
        avg_norm, avg = stats_lib.rolling_average(df, column, value_skip, normalization)
        df_rolling_average[column] = avg
        df_rolling_average_normalised[column] = avg_norm
    else:
        avg_norm, avg = stats_lib.rolling_average(df, column, value_skip)
        df_rolling_average[column] = avg
       
        
path_rolling_mean = 'Results/Rolling_Statistics/Rolling_Mean/long/' 
os.makedirs(path_rolling_mean)
        
stats_lib.plot_rolling_props(df_rolling_average, units, path_rolling_mean, 'mean', df_rolling_average_normalised)

'''
stand deviation
'''
df_rolling_std = pd.DataFrame()
df_rolling_std_norm = pd.DataFrame()

#calcullate 
for column in df.columns:
    normalisation = True
    std_norm, std = stats_lib.rolling_std(df, column, value_skip, normalisation)
    df_rolling_std[column] = std
    df_rolling_std_norm[column] = std_norm
    
path_rolling_std = 'Results/Rolling_Statistics/Rolling_Std/long/' 
os.makedirs(path_rolling_std)
        
stats_lib.plot_rolling_props(df_rolling_std, units, path_rolling_std, 'std', df_rolling_std_norm)

# %% Thrust Compariosons ex
path_sum = 'Results/Sum/'
Fex =  (df['Fx1'] + df['Fx2'] + df['Fx3']).to_numpy()
Thrust = (-1*df['Thrust']).to_numpy()
Fx = (-1*df['Fx']).to_numpy()
plt.plot(df.index[256:(256*2)], Thrust[256:(256*2)], label = 'Rotor')
plt.plot(df.index[256:(256*2)],Fex[256:(256*2)], label = 'Blades')
plt.plot(df.index[256:(256*2)], Fx[256:(256*2)], label = 'Base')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Amplitude (N)')
plt.title('Thrust Time Signal')
os.makedirs(path_sum)
plt.savefig(path_sum + 'force_ex_time' + '.png')
plt.close()

spectral_Fex = stats_lib.fft(Fex, 256, 256)
spectral_Thrust = stats_lib.fft(Thrust, 256, 256)
spectral_base = stats_lib.fft(Fx, 256, 256)
plt.plot(spectral_Fex, label = 'Blades')
plt.plot(spectral_base, label = 'Base')
plt.plot(spectral_Thrust, label = 'Rotor')
plt.legend()
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude[N]')
plt.yscale('log')
plt.title('FFT in ex direction')
plt.savefig(path_sum + 'force_ex_fft' + '.png')
plt.close()

# %% 