#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:42:23 2021

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
def access_file(file, run_time = 360, sampling_freq = 256):
    df = pd.read_csv(file, sep = '\t', skiprows=9, low_memory=False)
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
    

    t_per_meas = 1/sampling_freq
    #4160#4097#360#4097# 360#seconds
    no_of_meas = int(run_time / t_per_meas)
    # create time arra
    t = np.linspace(0, run_time, no_of_meas)
    #first add column to the data framce
    df['time'] = t
    #rename index to time values
    df = df.set_index('time')
    df['Thrust'] = -df['Thrust']
    df['Fx'] = -df['Fx']
    df['Torque'] = -df['Torque']
    df['Fy1'] = -df['Fy1']
    df['Mx1'] = -df['Mx1']
    df['My1'] = -df['My1']
    df['Fy2'] = -df['Fy2']
    df['Mx2'] = -df['Mx2']
    df['My2'] = -df['My2']
    df['Fy3'] = -df['Fy3']
    df['Mx3'] = -df['Mx3']
    df['My3'] = -df['My3']
    df['My'] = -df['My']
    
    
    return df

def stats(ser):
    #Statistics of the data
    std_val = ser.std(axis = 0)                    # standard deviation
    mean_val = ser.mean(axis = 0)                  # arithmatic mean
    max_val = ser.max(axis = 0)                    # max values
    min_val = ser.min(axis = 0)                    # min values
    return std_val, mean_val, max_val, min_val

def spectral_analysis(df, column, run_time = 360, sampling_freq = 256, bins = False):
    
    if bins == 'Default':
        
        bins = int(run_time*sampling_freq)
        timestep = df.index[1]
    else:
        timestep = df.index[1]
    
    spec = stats_lib.fft(df[column].to_numpy(), int(sampling_freq), int(bins))
    frequency = np.fft.fftfreq(int(bins), d=timestep)
    
    return spec, frequency

#function to cacluate rotor frequency to normalise fft
def rotor_freq(ser):
    return ser.mean()/60

# %% Filtrage Function
def filtrage(t,x,fc,filter_type):
    fe = 1/(t[1]-t[0])
    n = len(x)
    #not clear on why n-1 is used
    delta_f = fe/(n-1)
    f = np.arange(-fe/2, fe/2+delta_f, delta_f)
        #low pass filter
   
    f1 = min(fc)
    f2 = max(fc)

    ind1 = abs(f) < f1
    ind2 = abs(f) > f2
    ind = (ind1 + ind2)
    
    ind = np.fft.fftshift(ind)
    fftx = np.fft.fft(x)  
    fftx[ind == True] = 0
    xf = np.real(np.fft.ifft(fftx))
    return xf
# %% Anglue Turbine
def angle_turbine(t, Fy1, Fy2, Fy3, fr):
        
    f1 = fr - 0.2
    f2 = fr + 0.2
    

    Fy1=filtrage(t,Fy1-np.mean(Fy1),[f1, f2],3)
    Fy2=filtrage(t,Fy2-np.mean(Fy2),[f1, f2],3)
    Fy3=filtrage(t,Fy3-np.mean(Fy3),[f1, f2],3)    
    
    theta1=np.unwrap(np.arctan2((+np.sqrt(3)*Fy1),(Fy1+2*Fy2)))
    theta2=np.unwrap(np.arctan2(-(-np.sqrt(3)*Fy1),-(Fy1+2*Fy3)))
    theta3=np.unwrap(np.arctan2((-np.sqrt(3)*(Fy2+Fy3)),(Fy2-Fy3)))
    theta = np.mean(np.column_stack([theta1, theta2, theta3]), axis = 1)
    theta=theta-np.round(theta/(2*np.pi))*(2*np.pi)
    theta = theta * 180/np.pi + 180
    return theta