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
from Dashboard.data_import_func import access_file, angle_theta, polar_chart, angle_theta_binning, polar_chart_binning, phase_shift
import Dashboard.data_import_func
import stats_lib
import matplotlib.pyplot as plt
direc ='/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/'
files = np.sort(os.listdir(direc))[4:]
runs = np.append(files[145:155], [files[118], files[84], files[50], files[17]])
runs = np.insert(runs, 0, files[140])
dist = [93, 108, 123, 138, 153, 168, 183, 198, 213,228,243,260, 427, 594, 'Control']
# %%

#for binned and normalised. 
out_direc_bin_norm = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Binned_normalised_azimuthal/'

#binned and non-normalised
out_direc_bin_nnorm = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Binned_nonnormalised_azimuthal/'


#spline and normalised
out_direc_spl_norm = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Spline_normalised_azimuthal/'


#spline and non-normalised
out_direc_spl_nnorm = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/Spline_nonnormalised_azimuthal/'

for r,d in zip(runs,dist):
    df2, units = access_file(direc + r)
    
    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc_bin_norm+col):
            os.makedirs(out_direc_bin_norm + col)
            
        new_dir = out_direc_bin_norm + col
        polar_chart_binning(df2, col, True)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()
    

    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc_bin_nnorm+col):
            os.makedirs(out_direc_bin_nnorm + col)
            
        new_dir = out_direc_bin_nnorm + col
        polar_chart_binning(df2, col)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()


    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc_spl_norm + col):
            os.makedirs(out_direc_spl_norm + col)
            
        new_dir = out_direc_spl_norm + col
        polar_chart(df2, col, True)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()

    for col in df2.columns[1:]:
        if not os.path.isdir(out_direc_spl_nnorm + col):
            os.makedirs(out_direc_spl_nnorm + col)
            
        new_dir = out_direc_spl_nnorm + col
        polar_chart(df2, col)
        plt.title('Distance = {} mm, TSR = 4, Vel = 1.0 m/s'.format(d))
        plt.savefig(new_dir +'/' + str(d) + '.png', dpi = 300)
        plt.close()

# %% azimuthal subplots
#for binned and normalised. 
out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/Angular_Variation/'


column = ['Force', 'Couple']


for col in column:

    list_files = np.array_split(runs, 5)
    list_dist =np.array_split(dist, 5)      
    fig, ax = plt.subplots(2,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
    for i in range(len(ax)):
        for r,j,d in zip(list_files[i], range(3),list_dist[i]):
             df, _ = access_file(direc + r)
             angle, fit = angle_theta_binning(df, col)
             #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
             ax[i, j].plot(fit['theta'], fit['signal'], color = 'red')
             ax[i, j].set_rlabel_position(90)
             ax[i, j].set_theta_zero_location("N")  # theta=0 at the top
             ax[i, j].set_theta_direction(-1) 
             ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(3))
             if col == 'Couple':
                 ax[i, j].set_rticks([7.2, 7.4, 7.6])  # Less radial ticks
             elif col == 'Force':
                 ax[i, j].set_rticks([169, 172, 176])  # Less radial ticks
            
             ax[i,j].tick_params(axis='y', which='major', labelsize=9)
             ax[i, j].set_title('d = {:.2f}'.format(float(d)/724))
             
    plt.tight_layout()
    plt.savefig(out_direc + col + '_1.pdf')
    
    
    fig, ax = plt.subplots(2,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
    list_files = np.array_split(runs, 5)[2:4]
    list_dist =np.array_split(dist, 5)[2:4]
    for i in range(len(ax)):
        for r,j,d in zip(list_files[i], range(3),list_dist[i]):
             df, _ = access_file(direc + r)
             angle, fit = angle_theta_binning(df, col)
             #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
             ax[i, j].plot(fit['theta'], fit['signal'], color = 'red')
             ax[i, j].set_rlabel_position(90)
             ax[i, j].set_theta_zero_location("N")  # theta=0 at the top
             ax[i, j].set_theta_direction(-1) 
             ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(3))
             if col == 'Couple':
                 ax[i, j].set_rticks([7.2, 7.4, 7.6])  # Less radial ticks
             elif col == 'Force':
                 ax[i, j].set_rticks([169, 172, 176])  # Less radial ticks
            
             ax[i,j].tick_params(axis='y', which='major', labelsize=9)
             ax[i, j].set_title('d = {:.2f}'.format(float(d)/724))
    plt.tight_layout()
    plt.savefig(out_direc + col + '_2.pdf')
    
    
    fig, ax = plt.subplots(1,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
    list_files = np.array_split(runs, 5)[4]
    list_dist =np.array_split(dist, 5)[4]
    for r,j,d in zip(list_files, range(3),list_dist):
        df, _ = access_file(direc + r)
        angle, fit = angle_theta_binning(df, col)
             #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
        ax[j].plot(fit['theta'], fit['signal'], color = 'red')
        ax[j].set_rlabel_position(90)
        ax[j].set_theta_zero_location("N")  # theta=0 at the top
        ax[j].set_theta_direction(-1) 
        ax[j].yaxis.set_major_locator(plt.MaxNLocator(3))
        if col == 'Couple':
                 ax[j].set_rticks([7.2, 7.4, 7.6])  # Less radial ticks
        elif col == 'Force':
                 ax[j].set_rticks([169, 172, 176])  # Less radial ticks
            
        ax[j].tick_params(axis='y', which='major', labelsize=9)
        if d == 'Control':    
            ax[j].set_title('{}'.format(d))
        else:
            ax[j].set_title('d = {:.2f}'.format(float(d)/724))
    plt.tight_layout()
    plt.savefig(out_direc + col + '_3.pdf')

# %% Plotting Fx1, Fx2, and Fx3 on the same curve
list_files = np.array_split(runs, 5)
list_dist =np.array_split(dist, 5)      
fig, ax = plt.subplots(2,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
labels = ['TDC = 0$^\circ$']#, 'TDC = 120$^\circ$', 'TDC = 240$^\circ$']
for i in range(len(ax)):
    for r,j,d in zip(list_files[i], range(3),list_dist[i]):
         df, _ = access_file(direc + r)
         angle1, fit1 = angle_theta_binning(df, 'Fx1')
         #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
         a = ax[i, j].plot(fit1['theta'], fit1['signal'])[0]
         
         #angle2, fit2 = angle_theta_binning(df, 'Fx2')
         #b = ax[i, j].plot(fit2['theta'], fit2['signal'], linewidth = 1.0)[0]
         
         #angle3, fit3 = angle_theta_binning(df, 'Fx3')
         #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
         #c = ax[i, j].plot(fit3['theta'], fit3['signal'], linewidth = 1.0)[0]
         
         
         ax[i, j].set_rlabel_position(90)
         ax[i, j].set_theta_zero_location("N")  # theta=0 at the top
         ax[i, j].set_theta_direction(-1) 
         ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(3))
         ax[i, j].set_rticks([48, 52, 56, 60])  # Less radial ticks
         ax[i,j].tick_params(axis='y', which='major', labelsize=9)
         ax[i, j].set_title('d = {:.2f}'.format(float(d)/724))
#fig.legend([a, b, c], labels, loc = 'upper right')
plt.tight_layout()
plt.savefig(out_direc + 'Fx' + '_1.pdf')


fig, ax = plt.subplots(2,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
list_files = np.array_split(runs, 5)[2:4]
list_dist =np.array_split(dist, 5)[2:4]
for i in range(len(ax)):
    for r,j,d in zip(list_files[i], range(3),list_dist[i]):
         df, _ = access_file(direc + r)
         angle1, fit1 = angle_theta_binning(df, 'Fx1')
         #ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
         a = ax[i, j].plot(fit1['theta'], fit1['signal'])[0]
         
         
 #        angle2, fit2 = angle_theta_binning(df, 'Fx2')
         
  #       b = ax[i, j].plot(fit2['theta'], fit2['signal'], linewidth = 1.0)[0]
         
    #     angle3, fit3 = angle_theta_binning(df, 'Fx3')
    #      ax[i, j].scatter(angle['theta'], angle['signal'], s=0.01)
     #    c = ax[i, j].plot(fit3['theta'], fit3['signal'], linewidth = 1.0)[0]
         
         
         ax[i, j].set_rlabel_position(90)
         ax[i, j].set_theta_zero_location("N")  # theta=0 at the top
         ax[i, j].set_theta_direction(-1) 
         ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(3))
         ax[i, j].set_rticks([48, 52, 56, 60])  # Less radial ticks
         ax[i,j].tick_params(axis='y', which='major', labelsize=9)
         ax[i, j].set_title('d = {:.2f}'.format(float(d)/724))
#fig.legend([a, b, c], labels, loc = 'upper right')
plt.tight_layout()
plt.savefig(out_direc + 'Fx' + '_2.pdf')


fig, ax = plt.subplots(1,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
list_files = np.array_split(runs, 5)[4]
list_dist =np.array_split(dist, 5)[4]
for r,j,d in zip(list_files, range(3),list_dist):
    df, _ = access_file(direc + r)
    angle1, fit1 = angle_theta_binning(df, 'Fx1')
    a = ax[j].plot(fit1['theta'], fit1['signal'])[0]
    
    #angle2, fit2 = angle_theta_binning(df, 'Fx2')
    #b = ax[j].plot(fit2['theta'], fit2['signal'], linewidth = 1.0)[0]
    
    #angle3, fit3 = angle_theta_binning(df, 'Fx3')
    #c = ax[j].plot(fit3['theta'], fit3['signal'], linewidth = 1.0)[0]
         
    ax[j].set_rlabel_position(90)
    ax[j].set_theta_zero_location("N")  # theta=0 at the top
    ax[j].set_theta_direction(1) 
    ax[j].yaxis.set_major_locator(plt.MaxNLocator(3))
    ax[j].set_rticks([48, 52, 56, 60])  # Less radial ticks
    ax[j].tick_params(axis='y', which='major', labelsize=9)
    if d == 'Control':    
        ax[j].set_title('{}'.format(d))
    else:
        ax[j].set_title('d = {:.2f}'.format(float(d)/724))
#fig.legend([a, b, c], labels, loc = 'upper right')
plt.tight_layout()
plt.savefig(out_direc + 'Fx' + '_3.pdf')

# %% Azimuthal dry tests
drytest_direc = 'Dry_tests/run005.txt'
df, _ = access_file(drytest_direc)
column = ['Thrust', 'Torque']
fig, ax = plt.subplots(1,3,subplot_kw={'projection': 'polar'}, figsize=(60,60))
for col,i in zip(column, range(2)):
    angle, fit = angle_theta_binning(df, col)
    ax[i].plot(fit['theta'], fit['signal'], color = 'red')
    ax[i].set_rlabel_position(90)
    ax[i].set_theta_zero_location("N")  # theta=0 at the top
    ax[i].set_theta_direction(-1) 
    ax[i].yaxis.set_major_locator(plt.MaxNLocator(3))
    #ax[i].set_rticks([-4, -2, 0, 2, 4])  # Less radial ticks
    ax[i].tick_params(axis='y', which='major', labelsize=9)
    ax[i].set_title(col)
    

angle1, fit1 = angle_theta_binning(df, 'Fx1')
a = ax[2].plot(fit1['theta'], fit1['signal'])[0]


 
ax[2].set_rlabel_position(90)
ax[2].set_theta_zero_location("N")  # theta=0 at the top
ax[2].set_theta_direction(-1) 
ax[2].yaxis.set_major_locator(plt.MaxNLocator(3))
#ax[2].set_rticks([-4, -2, 0, 2, 4])  # Less radial ticks
ax[2].tick_params(axis='y', which='major', labelsize=9)
ax[2].set_title('Fx1')
#labels = ['TDC = 0$^\circ$', 'TDC = 120$^\circ$', 'TDC = 240$^\circ$']
#fig.legend([a, b, c],labels, loc = 'upper right')
plt.tight_layout()
plt.savefig(out_direc + 'dry_test.pdf')








# %%
a = phase_shift(angle2['signal'], 4 * np.pi/3)
angle2['shifted_s'] =a
fig = plt.figure()
ax = fig.add_subplot(projection = 'polar')

ax.scatter(angle2['theta'], angle2['signal'],s=0.01)
ax.scatter(angle1['theta'], angle1['signal'], s = 0.01)
plt.scatter(angle2['theta'], angle2['shifted_s'], s=0.01)

