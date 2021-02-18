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
run_time = 360 #seconds
no_of_meas = int(run_time / t_per_meas)
# create time array
t = np.linspace(0, run_time, no_of_meas)
#first add column to the data framce
df['time'] = t
#rename index to time values
df = df.set_index('time')

# %%
'''
Spectral Analysis using Welch Method. 
Comparison to be made with FFT
'''
path_welch = 'Documents/Github/Thesis_Tidal_Turbine/Results/Welch_Transform/'
for column in df:
    f, spectrum = signal.welch(df[column], fs = 256, window='hamm', noverlap=64)
    plt.plot(f, spectrum)
    plt.savefig(path_welch+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()

path_fft = 'Documents/Github/Thesis_Tidal_Turbine/Results/fft/'
freq_fft = np.linspace(0, 128, sampling_freq)
for  column in df:
    spectrum = fftpack.fft(df[column].to_numpy(), sampling_freq)
    plt.plot(freq_fft, abs(spectrum))
    plt.savefig(path_fft+column+'.png')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title(column)
    plt.close()

rolling_mean = df.rolling(5*sampling_freq).mean()
rolling_max = df.rolling(5*sampling_freq).max()
rolling_min = df.rolling(5*sampling_freq).min()
rolling_std = df.rolling(5*sampling_freq).std()


plt.plot(rolling_std['Thrust'])
path_rolling = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/'
for column in df:
    path_rolling = 'Documents/Github/Thesis_Tidal_Turbine/Results/Rolling_Statistics/' + column + '/'
    plt.plot()

spectrum = fftpack.fft(df['Thrust'].to_numpy(), 256)

plt.plot(abs(spectrum))
