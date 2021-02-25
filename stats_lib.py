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

def rolling_average(df, column_name: str):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []
    stat = np.append(stat, arr[0])
    
    for i in range(1,len(arr)):
        var = (arr[i] + stat[i - 1] * (len(stat)))/(i+1)
        stat = np.append(stat, var)
    return stat

def rolling_max(df, column_name):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []
    max_val = []
    for i in range(0, len(arr)):
        stat = np.append(stat, arr[i])
        max_val = np.append(max_val,max(stat))
    return max_val
 
def rolling_min(df, column_name):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []
    min_val = []
    for i in range(0, len(arr)):
        stat = np.append(stat, arr[i])
        min_val = np.append(min_val,min(stat))
    return min_val

def rolling_std(df, column_name):
    if not isinstance(column_name, str):
        raise TypeError
    arr = df[column_name].to_numpy()
    stat = []
    stat = np.append(stat, np.std(arr[0]))
    
    for i in range(1,len(arr)):
        var = (arr[i] + stat[i - 1] * (len(stat)))/(i+1)
        stat = np.append(stat, var)
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
        