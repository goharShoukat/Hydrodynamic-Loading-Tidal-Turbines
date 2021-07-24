#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 19:29:21 2021

@author: goharshoukat
function to calculate the coefficient of variation in velocity
"""

import pandas as pd
import numpy as np
import os
from Dashboard.load_ldv3D import load_ldv3D
import matplotlib.pyplot as plt
direc ='/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/essais_ifremer_04_2021_backup/LDV/2021_04_hydrol_ECN/'
files = np.sort(os.listdir(direc))[6:]
runs = np.append(files[144:154], [files[117], files[83], files[50]])
runs = np.insert(runs, 0, files[139])
dist = [93, 108, 123, 138, 153, 168, 183, 198, 213,228,243,260, 427, 594]
output = '/Users/goharshoukat/Documents/GitHub/Thesis_Tidal_Turbine/'
df = pd.DataFrame(columns = ['u avg', 'sigma u', 'u^2 avg', 'sigma u^2', 'u^3 avg', 'sigma u^3'], index=(dist))

for r,ind in zip(runs, df.index):
    t, u = load_ldv3D(direc+r,0)
    df.loc[ind]['u avg'] = np.mean(u)
    df.loc[ind]['sigma u'] = np.std(u)
    df.loc[ind]['u^2 avg'] = np.mean(u**2)
    df.loc[ind]['sigma u^2'] = np.std(u**2)
    df.loc[ind]['u^3 avg'] = np.mean(u**3)
    df.loc[ind]['sigma u^3'] = np.std(u**3)
df['Reletive Position'] = df.index

# %% U
error_u = df['sigma u']
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df['Reletive Position']/724, df['u avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df['Reletive Position'], df['u avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax1.set_ylabel(r'$U (m/s)$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.title('TSR = 4, Velocity = 1.0 m/s')
plt.savefig(output + 'Results/Velocity/Velocity.png', dpi = 300)
plt.close()

# %% U**2
error_u = df['sigma u^2']
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df['Reletive Position']/724, df['u^2 avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df['Reletive Position'], df['u^2 avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax1.set_ylabel(r'$U \times U (m2/s2)$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.title('TSR = 4, Velocity = 1.0 m/s')
plt.savefig(output + 'Results/Velocity/Velocity_squared.png', dpi = 300)
plt.close()
# %% U**3
error_u = df['sigma u^3']
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df['Reletive Position']/724, df['u^3 avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df['Reletive Position'], df['u^3 avg'], error_u, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax1.set_ylabel(r'$U \times U \times U (m3/s3)$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.title('TSR = 4, Velocity = 1.0 m/s')
plt.savefig(output + 'Results/Velocity/Velocity_cubed.png', dpi = 300)
plt.close()
# %% Coefficient of Variation u

#plot coefficient of variation against position without mean values
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny() #for normalised mast position
#ax3 = ax1.twinx() #for normalised standard deviation
ax1.plot((df['Reletive Position'])/724, df['sigma u']/df['u avg'] * 100, 'o--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax2.plot(df['Reletive Position'], df['sigma u']/df['u avg'] * 100, 'o--')
#x2.plot(df['Reletive Position'], df['sigma u']/df['u avg'], 'o--')
#ax3.plot(df2['Reletive Position']/724, df2['Cp sigma'], 'go--', label = '$C_p$')
#ax3.plot(df2['Reletive Position']/724, df2['Ct sigma'], 'o--', label = '$C_t$')
#ax3.set_ylabel(r'$\sigma$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax1.set_ylabel(r'Coefficient of Variation  $\frac{\sigma}{\mu} (\%)$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax2.legend()
#ax3.legend()
ax1.grid('both')
ax2.grid(False)
#ax3.grid(False)
plt.savefig(output + 'Results/Velocity/U COV.png', dpi = 600)
plt.close()

# %% # %% Coefficient of Variation u^2

#plot coefficient of variation against position without mean values
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny() #for normalised mast position
#ax3 = ax1.twinx() #for normalised standard deviation
ax1.plot((df['Reletive Position'])/724, df['sigma u^2']/df['u^2 avg'] * 100, 'o--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax2.plot(df['Reletive Position'], df['sigma u^2']/df['u^2 avg'] * 100, 'o--')
#x2.plot(df['Reletive Position'], df['sigma u']/df['u avg'], 'o--')
#ax3.plot(df2['Reletive Position']/724, df2['Cp sigma'], 'go--', label = '$C_p$')
#ax3.plot(df2['Reletive Position']/724, df2['Ct sigma'], 'o--', label = '$C_t$')
#ax3.set_ylabel(r'$\sigma$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax1.set_ylabel(r'Coefficient of Variation  $\frac{\sigma}{\mu} (\%)$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax2.legend()
#ax3.legend()
ax1.grid('both')
ax2.grid(False)
#ax3.grid(False)
plt.savefig(output + 'Results/Velocity/U^2 COV.png', dpi = 600)
plt.close()


# %% # %% Coefficient of Variation u^3

#plot coefficient of variation against position without mean values
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny() #for normalised mast position
#ax3 = ax1.twinx() #for normalised standard deviation
ax1.plot((df['Reletive Position'])/724, df['sigma u^3']/df['u^3 avg'] * 100, 'o--')
ax1.set_xticks(np.linspace(np.min(df['Reletive Position']/724), np.max((df['Reletive Position']/724)), 10))
ax2.plot(df['Reletive Position'], df['sigma u^3']/df['u^3 avg'] * 100, 'o--')
#x2.plot(df['Reletive Position'], df['sigma u']/df['u avg'], 'o--')
#ax3.plot(df2['Reletive Position']/724, df2['Cp sigma'], 'go--', label = '$C_p$')
#ax3.plot(df2['Reletive Position']/724, df2['Ct sigma'], 'o--', label = '$C_t$')
#ax3.set_ylabel(r'$\sigma$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax1.set_ylabel(r'Coefficient of Variation  $\frac{\sigma}{\mu} (\%)$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax2.legend()
#ax3.legend()
ax1.grid('both')
ax2.grid(False)
#ax3.grid(False)
plt.savefig(output + 'Results/Velocity/U^3 COV.png', dpi = 600)
plt.close()

