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

def exceedence(df, content, plot = False):
    #takes in the raw data file as input
    #content : string : the signal for which exceedence is needed
    #plot : string : Boolean. if true, plot is also displayed
    #outputs the exceedence curve : array
    #outputs the array for which the exceedence is calculated : array

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
files = np.sort(os.listdir(directory))[4:]
runs = np.append(files[145:155], [files[118], files[84], files[50]])
runs = np.insert(runs, 0, files[140])
runs = runs[0:13:2]
runs = np.insert(runs, 1, files[145])
dist = np.array([93, 108, 123, 138, 153, 168, 183, 198, 213,228,243,260, 427, 594])/724
dist_ = dist[0:14:2]
dist = np.insert(dist_, 1, dist[1])
signals = ['Fx1', 'Fx2', 'Fx3', 'My1', 'My2', 'My3', 'Force', 'Couple']
summary = pd.read_csv('Cp_Ct/Experiment_Summary.csv')


for content in signals:
    fig = plt.figure(figsize = (60,60))
    for r,d in zip(runs,dist):
        df, _ = access_file(directory + r)
        mean1, exced1 = exceedence(df, content)
        
        plt.semilogy(mean1, exced1, label = '{:.2f}'.format(d))
        plt.legend()
        plt.xlabel(r'X/$\bar{X}$')
        plt.ylabel('Exceedence Probability')
        plt.grid(True, which = 'minor')
        plt.grid(True, which = 'major')
        plt.title(content)
        
        
       # plt.xticks(np.linspace(np.min(mean1), np.max(mean1), 10))
        #mean2, exced2 = exceedence(directory + runs[1], content)
        #plt.semilogy(mean2, exced2)
    plt.savefig(output_directory + content + '.pdf')
    plt.close()

