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
#%%
'''
File Read into script
Data Cleaning, Time Stamp Addition
Simple Statistics Calculated
Initial Plots
'''

#The data file was cleaned to remove the first couple of lines. 
path = 'Documents/Github/Thesis_Tidal_Turbine/Prior_Data_Papers/'
df = pd.read_csv(path+'run007.txt', sep = '\t', skiprows=9)
df = df.drop([0])
#renaming first column header
df = df.rename({'#RPM': 'RPM'}, axis=1)
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
run_time = 360#4097#360 #seconds
no_of_meas = int(run_time / t_per_meas)
# create time arra
t = np.linspace(0, run_time, no_of_meas)
#first add column to the data framce
df['time'] = t
#rename index to time values
df = df.set_index('time')

# %% Spectral Analysis

path_fft = 'Documents/Github/Thesis_Tidal_Turbine/Results/fft/'
os.makedirs(path_fft)
frequency = np.linspace(0, int(sampling_freq/2), int(no_of_meas/2))

for  column in df:
    if column == 'RPM':
        pass
    else:
        freq_data = fftpack.fft(df[column].to_numpy())
        y = 2/no_of_meas * np.abs(freq_data[0:np.int(no_of_meas/2)])
        y[0] = y[0] / 2
        fig = plt.plot(frequency, y)
        plt.yscale('log')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.title(column)
        plt.grid(True, which = 'both', linestyle='--')
        plt.savefig(path_fft+column+'.png')
        pickle.dump(fig, open(path_fft+column + 'fig.pickle','wb'))
        plt.close()
# %%
'''
Spectral Analysis using Welch Method. 
Comparison to be made with FFT
'''
'''
path_welch = 'Documents/Github/Thesis_Tidal_Turbine/Results/Welch_Transform/'
os.makedirs(path_welch)
for column in df:
    f, spectrum = signal.welch(df[column], fs = 256, window='hamm', noverlap=64)
    plt.plot(f, spectrum)
    plt.savefig(path_welch+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
'''
# %%
rolling_mean = df.rolling(10*sampling_freq).mean()
rolling_rolling_mean = rolling_mean.rolling(7).std()

rolling_max = df.rolling(10*sampling_freq).max()
rolling_rolling_max = rolling_max.rolling(7).std()


rolling_min = df.rolling(10*sampling_freq).min()
rolling_rolling_min = rolling_min.rolling(7).std()

rolling_std = df.rolling(10*sampling_freq).std()
rolling_rolling_std = rolling_std.rolling(7).std()

path_rolling_mean = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Mean/' 
os.makedirs(path_rolling_mean)

path_rolling_max = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Max/'
os.makedirs(path_rolling_max)

path_rolling_min = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Min/' 
os.makedirs(path_rolling_min)

path_rolling_std = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Std/'
os.makedirs(path_rolling_std)
    
for column in df:
    plt.plot(rolling_rolling_mean[column])
    plt.savefig(path_rolling_mean+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_rolling_max[column])
    plt.savefig(path_rolling_max+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_rolling_min[column])
    plt.savefig(path_rolling_min+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_rolling_std[column])
    plt.savefig(path_rolling_std+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
# %%
rolling_mean = df.rolling(10*sampling_freq).mean()


rolling_max = df.rolling(10*sampling_freq).max()


rolling_min = df.rolling(10*sampling_freq).min()


rolling_std = df.rolling(10*sampling_freq).std()


path_rolling_mean = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Mean/' 
os.makedirs(path_rolling_mean)

path_rolling_max = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Max/'
os.makedirs(path_rolling_max)

path_rolling_min = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Min/' 
os.makedirs(path_rolling_min)

path_rolling_std = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/Rolling_Std/'
os.makedirs(path_rolling_std)
    
plt.plot(rolling_mean['Thrust'][1000:2000])
for column in df:
    plt.plot(rolling_mean[column])
    plt.savefig(path_rolling_mean+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_max[column])
    plt.savefig(path_rolling_max+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_min[column])
    plt.savefig(path_rolling_min+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()
    
    plt.plot(rolling_std[column])
    plt.savefig(path_rolling_std+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()