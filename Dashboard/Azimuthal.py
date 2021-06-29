#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 19:25:20 2021

@author: goharshoukat
"""
    
from sklearn.preprocessing import scale
import pandas as pd
import numpy as np
import os
from Dashboard.data_import_func import access_file, angle_theta, polar_chart, angle_theta_binning, polar_chart_binning
import Dashboard.data_import_func
import stats_lib
import matplotlib.pyplot as plt
direc ='/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/'
files = np.sort(os.listdir(direc))[4:]
df, units = access_file(direc + files[75])
runs = np.append(files[144:155], [files[118], files[84], files[50]])
dist = [93, 108, 123, 138, 153, 168, 183, 198, 213,228,243,260, 427, 594]
# %%


# %%

out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Azimuthal/Azimuthal/'

#for binned and normalised. 

for r,d in zip(runs,dist):
    df2, units = access_file(direc + r)
    
    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc+col):
            os.mkdir(out_direc + col)
            
        new_dir = out_direc + col
        polar_chart_binning(df2, col, True)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()
    

#binned and non-normalised
out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Binned_nonnormalised_azimuthal/'

for r,d in zip(runs,dist):
    df2, units = access_file(direc + r)
    
    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc+col):
            os.mkdir(out_direc + col)
            
        new_dir = out_direc + col
        polar_chart_binning(df2, col)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()


#spline and normalised
out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Spline_normalised_azimuthal/'

for r,d in zip(runs,dist):
    df2, units = access_file(direc + r)
    
    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc+col):
            os.mkdir(out_direc + col)
            
        new_dir = out_direc + col
        polar_chart(df2, col, True)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()

#spline and normalised
out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Spline_nonnormalised_azimuthal/'

for r,d in zip(runs,dist):
    df2, units = access_file(direc + r)
    
    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc+col):
            os.mkdir(out_direc + col)
            
        new_dir = out_direc + col
        polar_chart(df2, col)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()



