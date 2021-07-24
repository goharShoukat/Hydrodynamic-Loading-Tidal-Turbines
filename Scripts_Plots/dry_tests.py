#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 19:23:47 2021

@author: goharshoukat

This sript analyses the dry tests to identify the cause of the noise in the fft signal

"""
import numpy as np
import pandas as pd
from Dashboard.data_import_func import access_file, spectral_analysis, rotor_freq
import matplotlib.pyplot as plt

direc = 'Dry_tests/run005.txt'
df, units = access_file(direc)
column = ['Fx1', 'Thrust', 'Torque', 'My1']
for col in column:
    fig= plt.figure(figsize=(60,60))
    ax = fig.add_subplot(111)
    spec_s, f_s = spectral_analysis(df, col, bins = 'Default')
    rfreq = rotor_freq(df['#RPM'])
    freq_s = f_s/rfreq
    ax.loglog(freq_s, spec_s[1:], linewidth = 0.8)
    ax.minorticks_on()
    ax.grid(which = 'minor', linestyle='--')
    ax.grid(which = 'major', linestyle = '-')
    #plt.title('{}, TSR = 4.0, Dry Test'.format(col))
    ax.set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')
    ax.set_ylabel('Magnitude ({})'.format(units[col]))
    plt.savefig('Results/fft/Dry_tests/' + col + '.pdf')
    