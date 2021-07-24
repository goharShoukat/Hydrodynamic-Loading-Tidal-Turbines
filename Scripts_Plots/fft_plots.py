#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 15:37:38 2021

@author: goharshoukat

Generate subplots for fft with multiple fft on the same plot
"""

import pandas as pd
import numpy as np
import os
from Dashboard.data_import_func import access_file, rotor_freq, spectral_analysis
import Dashboard.data_import_func
import stats_lib
import matplotlib.pyplot as plt
from Dashboard.load_ldv3D import load_ldv3D
from scipy.signal import find_peaks
direc ='/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/2021_04_hydrol_ECN/'
files = np.sort(os.listdir(direc))[4:]
runs = np.append(files[145:155], [files[118], files[84], files[50], files[17]])
runs = np.insert(runs, 0, files[140])
dist = [93, 108, 123, 138, 153, 168, 183, 198, 213,228,243,260, 427, 594, 'Control']

#noise spectral analysis
def spectral_analysis_noisy(df, column, bins = False):
    
    if bins == 'Default':
        
        bins = len(df)
        timestep = df.index[1]
    else:
        timestep = df.index[1]
    sampling_freq = 1/timestep
    spec = stats_lib.fft(df[column].to_numpy(), int(sampling_freq), int(bins))
    frequency = np.fft.fftfreq(int(bins), d=timestep)

    return spec, frequency

# %% For loop

out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/fft/'

column = ['Fx1', 'Force', 'Couple', 'My1']
list_files = np.array_split(runs, 5)[:3]
list_dist =np.array_split(dist, 5)[:3]
for col in column:
        
    fig, ax = plt.subplots(3,1, figsize=(60,60), sharex = True)

    for i in range(len(ax)):
        for r,d in zip(list_files[i], list_dist[i]):
            df, units = access_file(direc+r)
            spec_s, f_s = spectral_analysis(df, col, bins = 'Default')
            rfreq = rotor_freq(df['RPM'])
            freq_s = f_s/rfreq
            ax[i].loglog(freq_s, spec_s[1:], linewidth = 0.8, label = '{} mnm'.format(d))
            ax[i].minorticks_on()
            ax[i].grid(which = 'minor', linestyle='--')
            ax[i].grid(which = 'major', linestyle = '-')
            ax[i].legend()
        ax[i].set_ylabel('Magnitude ({})'.format(units[col]))
    ax[2].set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')   
    plt.savefig(out_direc + col +'_1.pdf')        
            
    
    fig, ax = plt.subplots(2,1, figsize=(60,60), sharex = True)
    list_files = np.array_split(runs, 5)[3:]
    list_dist =np.array_split(dist, 5)[3:]
    for i in range(len(ax)):
        for r,d in zip(list_files[i], list_dist[i]):
            df, units = access_file(direc+r)
            spec_s, f_s = spectral_analysis(df, col, bins = 'Default')
            rfreq = rotor_freq(df['RPM'])
            freq_s = f_s/rfreq
            if not d == 'Control':
                ax[i].loglog(freq_s, spec_s[1:], linewidth = 0.8, label = '{} mm'.format(d))
            else:
                ax[i].loglog(freq_s, spec_s[1:], linewidth = 0.8, label = '{}'.format(d))
            ax[i].minorticks_on()
            ax[i].grid(which = 'minor', linestyle='--')
            ax[i].grid(which = 'major', linestyle = '-')
            ax[i].legend()
        ax[i].set_ylabel('Magnitude ({})'.format(units[col]))
    ax[1].set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')   
    plt.savefig(out_direc + col + '_2.pdf')        
        
        
            

# %% only 3 on the same figure
out_direc = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/Results/fft/'
#dist = [93/724, 108/724, 'Control']
#new_runs = np.array([runs[0], runs[1], runs[-1]])
dist = [93/724, 'Control']
new_runs = np.array([runs[0], runs[-1]])

column = ['Fx1', 'Force', 'Couple', 'My1']
for col in column:
        
    fig, ax = plt.subplots(1,1, figsize=(60,60))
    for r,d in zip(new_runs,dist):
        df, units = access_file(direc+r)
        spec_s, f_s = spectral_analysis(df, col, bins = 'Default')
        rfreq = rotor_freq(df['RPM'])
        freq_s = f_s/rfreq
        if not d == 'Control':
            ax.loglog(freq_s, spec_s[1:], linewidth = 0.7, label = 'd = {:.2f}'.format(d))
        else:
            ax.loglog(freq_s, spec_s[1:], linewidth = 0.7, label = '{}'.format(d))

    ax.minorticks_on()
    ax.grid(which = 'minor', linestyle='--')
    ax.grid(which = 'major', linestyle = '-')
    ax.legend()
    ax.set_ylabel('Magnitude ({})'.format(units[col]))
    ax.set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')  
    plt.savefig(out_direc + col + '.pdf')

# %% Velocity Spectrum
direc_vel = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/LDV/2021_04_hydrol_ECN/'
vel_runs = np.array(['run141.000001.txt', 'run150.000001.txt', 'run018.000001.txt'])
runs = np.array(['run141.txt', 'run150.txt', 'run018.txt'])
dist = [93/724, 168/724, 'Control']
for r_vel,r,d in zip(vel_runs, runs, dist):
    df, _ = access_file(direc + r)
    t, u = load_ldv3D(direc_vel+r_vel,0)
    df_vel = pd.DataFrame(u, index = t, columns=['Velocity'])
    spec_s, f_s = spectral_analysis(df_vel, 'Velocity', bins = 'Default')
    rfreq = rotor_freq(df['RPM'])
    freq_s = f_s/rfreq

    if not d == 'Control':
            plt.loglog(freq_s, spec_s[1:], linewidth = 0.8, label = 'd = {:.2f}'.format(d))
    else:
            plt.loglog(freq_s, spec_s[1:], linewidth = 0.8, label = '{}'.format(d))
plt.minorticks_on()
plt.grid(which = 'minor', linestyle='--')
plt.grid(which = 'major', linestyle = '-')
plt.ylabel('Magnitude [m/s]')
plt.xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]') 
plt.legend()
plt.savefig(out_direc + 'vel_spec.pdf')
# %% combined fft and vel spectrum
direc_vel = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/LDV/2021_04_hydrol_ECN/'
vel_runs = np.array(['run141.000001.txt', 'run018.000001.txt'])
runs = np.array(['run141.txt', 'run018.txt'])
dist = [93/724, 'Control']
column = ['Fx1', 'Force', 'Couple', 'My1']

for col in column:
    fig, ax = plt.subplots(2,1, figsize=(60,60), sharex = True)
            
    for r, d, r_vel in zip(runs, dist, vel_runs):
        df, units = access_file(direc+r)
        spec_s, f_s = spectral_analysis(df, col, bins = 'Default')
        rfreq = rotor_freq(df['RPM'])
        freq_s = f_s/rfreq
        if not d == 'Control':
            ax[0].loglog(freq_s, spec_s[1:], linewidth = 0.8, label = 'd = {:.2f}'.format(d))
        else:
            ax[0].loglog(freq_s, spec_s[1:], linewidth = 0.8, label = '{}'.format(d))

        
        t, u = load_ldv3D(direc_vel+r_vel,0)
        df_vel = pd.DataFrame(u, index = t, columns=['Velocity'])
        spec_s_vel, f_s_vel = spectral_analysis(df_vel, 'Velocity', bins = 'Default')
        freq_vel = f_s_vel/rfreq
        
        if not d == 'Control':
            ax[1].loglog(freq_vel, spec_s_vel[1:], linewidth = 0.8)
        else:
            ax[1].loglog(freq_vel, spec_s_vel[1:], linewidth = 0.8)
        
        
        
    ax[1].minorticks_on()
    ax[1].grid(which = 'minor', linestyle='--')
    ax[1].grid(which = 'major', linestyle = '-')
    ax[1].set_ylabel('Magnitude (m/s)')
        
    ax[0].minorticks_on()
    ax[0].grid(which = 'minor', linestyle='--')
    ax[0].grid(which = 'major', linestyle = '-')
    ax[0].set_ylabel('Magnitude ({})'.format(units[col]))
    ax[1].set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')
    fig.legend(loc = 'upper right')
    plt.savefig(out_direc + col + '.pdf')
    
data = np.array([freq_s, spec_s[1:]]).T
df2= pd.DataFrame(data, columns=['Frequency', 'Spectrum'])


peaks, _ = find_peaks(df2['Spectrum'], height = 0.0003, distance = 500)
plt.loglog(df2['Frequency'], df2['Spectrum'], alpha = 0.8)
df2['Frequency'][df2['Spectrum'][peaks].index]
plt.loglog(df2['Frequency'][df2['Spectrum'][peaks].index], df2['Spectrum'][peaks], 'x')

labels = ['', 'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I']