#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 13:19:43 2021

@author: 
    
Function to calculate and plot exceedence curves
"""

from Dashboard.data_import_func import access_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def exceedence(file, content, plot = False):
    #takes in the raw data file as input
    #content : string : the signal for which exceedence is needed
    #plot : string : Boolean. if true, plot is also displayed
    #outputs the exceedence curve : array
    #outputs the array for which the exceedence is calculated : array
    
    
    df, _ = access_file(file)
    mean = df.mean(axis = 0)
    maxima = df.max(axis = 0)/mean #needed to define the upper limit of array
    minima = df.min(axis = 0)/mean #defines lower limit for which exceedence is calculated
    mean_array = np.linspace(minima[content], maxima[content], 100)
    exceedence = []
    for i in range(len(mean_array)):
        d = df[content] / mean[content] < mean_array[i] #checks which value is above or below the value in the array
        x = 1 - sum(d) / len(df) #first fins total number of values in the df which exceed the stated value in the array. then finds the probability of the true values. then subtracts  from 1 to find the exceedence
        exceedence.append(x) #push it into the array which is then returned
        
    if plot == True:
        #fig = plt.figure(figsize = (20,10))
        plt.semilogy(mean_array, exceedence)
        plt.xlabel(r'X/$\bar{X}$')
        plt.ylabel('Exceedence Probability')
        plt.grid('both')
        plt.title(content)
    return mean_array, exceedence


#create an for loop for plotting exceedence curves for Fx1, Fy1, My1, Couple and Thrust
directory = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/'
output_directory = 'Results/Exceedence/'

files = np.sort(os.listdir(directory))[149:159] 
signals = ['Fx1', 'Fx2', 'Fx3', 'My1', 'My2', 'My3', 'Force', 'Couple']
summary = pd.read_csv('Cp_Ct/Experiment_Summary.csv')

for file in files:
    if not os.path.isdir(output_directory + summary[summary['Original'] == file[:-4]]['Force File Name'].iloc[0]):
        os.mkdir(output_directory + summary[summary['Original'] == file[:-4]]['Force File Name'].iloc[0])
        
    for content in signals:
        mean, exced = exceedence(directory + file, content)
        #fig = plt.figure(figsize = (20,10))
        plt.semilogy(mean, exced)
        plt.xlabel(r'X/$\bar{X}$')
        plt.ylabel('Exceedence Probability')
        plt.grid('both')
        plt.title(summary[summary['Original'] == file[:-4]]['Force File Name'].iloc[0] + '-' + content)
        plt.savefig(output_directory + summary[summary['Original'] == file[:-4]]['Force File Name'].iloc[0] + '/' + content + '.png')
        plt.close()
        
'''
file = 'run149.txt'
df, _ = exceedence('/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/' + file, 'Force', plot = True)
    



file = 'run145.txt'
df, units = access_file('/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/' + file)
mean = df.mean(axis = 0)
maxima = df.max(axis = 0)/mean
minima = df.min(axis = 0)/mean



mean_array = np.linspace(minima['Force'], maxima['Force'], 100)


exceedence = []

for i in range(len(mean_array)):
    d = df['Force']/mean['Force'] < mean_array[i] 
    x = 1-sum(d)/len(df)
    exceedence.append(x)

plt.semilogy(mean_array, exceedence)
plt.grid('both')
'''