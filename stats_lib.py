#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:02:01 2021

@author: goharshoukat
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def rolling_average(df, column_name: str, value_skip, normalization=False):
    if not isinstance(column_name, str):
        raise TypeError
    if not isinstance(normalization, bool):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []
    stat = np.append(stat, arr[0])
    
    for i in range(1,len(arr), value_skip):
        var = (arr[i] + stat[int(i/value_skip) - 1] * (len(stat)))/(len(stat)+1)
        stat = np.append(stat, var)
    
    if normalization == True:
        mean = np.mean(arr)
        stat_norm = stat/mean
        return stat_norm, stat
    else:
        return stat



def rolling_std(df, column_name, value_skip, normalization= False):
    if not isinstance(column_name, str):
        raise TypeError
    if not isinstance(normalization, bool):
        raise TypeError
    
    arr = df[column_name].to_numpy()
    #the dummy array holds the sampled array
    dummy = []
    
    for i in range(0, len(arr), value_skip):
        dummy = np.append(dummy, arr[i])
    
    stat = []
    
    for i in range(0, len(arr)):
        var = np.std(dummy[0:(i+1)])
        stat = np.append(stat, var)
    
    if normalization==True:
        mean = np.mean(arr)
        stat_norm = stat/mean
        return stat_norm, stat
    else:
        return stat
        
    
        
        
def rolling_max(df, column_name):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []   
    stat = np.append(stat, arr[0])

    for i in range(1, len(arr)):
        if stat[i-1] > arr[i]:
            stat = np.append(stat, stat[i-1])
        else:
            stat = np.append(stat, arr[i])
    return stat
 


def rolling_min(df, column_name):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []   
    stat = np.append(stat, arr[0])

    for i in range(1, len(arr)):
        if stat[i-1] < arr[i]:
            stat = np.append(stat, stat[i-1])
        else:
            stat = np.append(stat, arr[i])
    return stat
   
    

        
def plot_rolling_props(df, units, path, prop):
    if prop == 'mean':        
        for column in df.columns:        
            plt.plot(df.index, df[column])
            plt.title(column)
            plt.xlabel('time (s)')
            plt.ylabel(r'$\mu$' + '(' + units[column]+ ')')
            plt.grid()
            plt.close()
        
    elif prop == 'max' or 'min':
        for column in df.columns:        
            plt.plot(df.index, df[column])
            plt.title(column)
            plt.xlabel('time (s)')
            plt.ylabel(units[column])
            plt.grid()
            plt.savefig(path + column + '.png')
            plt.close()
    else:
        for column in df.columns:        
            plt.plot(df.index, df[column])
            plt.title(column)
            plt.xlabel('time (s)')
            plt.ylabel(r'$\sigma$' + '(' + units[column]+ ')')
            plt.grid()
            plt.close()