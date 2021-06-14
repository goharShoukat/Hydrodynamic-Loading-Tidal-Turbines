#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:29:50 2021

@author: goharshoukat
"""

#TSR4 sensitivity analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from Dashboard.load_ldv3D import load_ldv3D
from Dashboard.data_import_func import access_file
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

path = 'Cp_Ct/'
df = pd.read_csv(path+'Experiment_Summary.csv')

#dataframe with the information regarding TSR 4 only
df2 = df[((df['TSR'] == '4,00') | (df['TSR'] == '4,0')) & (df['Velocity'] == '1')]
df2 = df2.reset_index(drop = True)
#important to convert the comma to decimal for python to interpret it as a floating point
#convert the strings to floating point to sort the column for plotting
df2['Reletive Position'] = df2['Reletive Position'].str.replace(',','.').astype(float)
#drop rows with information about the long runs. 
df2 = df2.drop(df2[df2['Force File Name'].str.contains('LR')].index)
df2 = df2.sort_values('Reletive Position')


# %%
#plot Reletive Position against Cp
error_Cp = df2['Cp sigma']
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Cp mean'], error_Cp, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df2['Reletive Position'], df2['Cp mean'], error_Cp, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax1.set_ylabel(r'$C_p$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.show()
plt.savefig('Results/Performance Coefficients/TSR4/Cp.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, eb1, eb2

fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Ct mean'], df2['Ct sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df2['Reletive Position'], df2['Ct mean'], df2['Ct sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax1.set_ylabel(r'$C_t$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.show()
plt.savefig('Results/Performance Coefficients/TSR4/Ct.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, eb1, eb2

#plot coefficient of variation against position without mean values
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny() #for normalised mast position
#ax3 = ax1.twinx() #for normalised standard deviation
ax1.plot((df2['Reletive Position'])/724, df2['Cp sigma']/df2['Cp mean'], 'o--', label = 'Normalised $C_p$')
ax1.plot((df2['Reletive Position'])/724, df2['Ct sigma']/df2['Ct mean'], 'o--', label = 'Normalised $C_t$')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax2.plot(df2['Reletive Position'], df2['Cp sigma']/df2['Cp mean'], 'o--')
ax2.plot(df2['Reletive Position'], df2['Ct sigma']/df2['Ct mean'], 'o--')
#ax3.plot(df2['Reletive Position']/724, df2['Cp sigma'], 'go--', label = '$C_p$')
#ax3.plot(df2['Reletive Position']/724, df2['Ct sigma'], 'o--', label = '$C_t$')
#ax3.set_ylabel(r'$\sigma$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax1.set_ylabel(r'Coefficient of Variation $\frac{\sigma}{\mu}$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax2.legend()
#ax3.legend()
ax1.grid('both')
ax2.grid(False)
#ax3.grid(False)
plt.savefig('Results/Performance Coefficients/TSR4/Cp Ct Coefficient of Variation.png', dpi = 600)
plt.close()
del fig2, ax1, ax2


#plot standard deviation against position without mean values
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny() #for normalised mast position
ax1.plot((df2['Reletive Position'])/724, df2['Cp sigma'], 'o--', label = '$C_p$')
ax1.plot((df2['Reletive Position'])/724, df2['Ct sigma'], 'o--', label = '$C_t$')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax2.plot(df2['Reletive Position'], df2['Cp sigma'], 'o--')
ax2.plot(df2['Reletive Position'], df2['Ct sigma'], 'o--')
ax1.set_ylabel(r'$\sigma$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax2.legend()
#ax3.legend()
ax1.grid('both')
ax2.grid(False)
#ax3.grid(False)
plt.savefig('Results/Performance Coefficients/TSR4/Cp Ct Standard Deviation.png', dpi = 600)
plt.close()
del fig2, ax1, ax2

# %%
#plot torque against 
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Torque_mean'], df2['Torque sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df2['Reletive Position'], df2['Torque_mean'], df2['Torque sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax1.set_ylabel(r'Torque $\frac{N}{m}$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.show()
plt.savefig('Results/Performance Coefficients/TSR4/Torque.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, eb1, eb2

fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
ax3 = ax1.twinx()
ax1.plot(df2['Reletive Position']/724, df2['Torque sigma']/df2['Torque_mean'], 'ro--', label = 'Coefficient of Variation')
ax2.plot(df2['Reletive Position'], df2['Torque sigma']/df2['Torque_mean'], 'ro--')
ax3.plot(df2['Reletive Position']/724, df2['Torque sigma'], 'bo--', label = 'Standard Deviation')
#plot standar deviation against position without mean values
ax1.set_ylabel(r'Coefficient of Variation $\frac{\sigma}{\mu}$')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
ax3.set_ylabel(r'$\sigma$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.grid('both')
ax2.grid(False)
ax3.grid(False)
plt.show()
ax1.legend(bbox_to_anchor=(1,1), loc = 1)
ax3.legend(bbox_to_anchor = (0.7,1), loc = 2)
plt.savefig('Results/Performance Coefficients/TSR4/Torque Standard Deviation.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, ax3
# %%
#plot thrust against  

fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Thrust_mean'], df2['Thrust sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df2['Reletive Position'], df2['Thrust_mean'], df2['Thrust sigma'], fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max((df2['Reletive Position']/724)), 10))
ax1.set_ylabel(r'Thrust $N$')
ax1.grid('both')
ax2.grid(False)
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
plt.show()
plt.savefig('Results/Performance Coefficients/TSR4/Thrust.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, eb1, eb2

fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
ax3 = ax1.twinx()
ax1.plot(df2['Reletive Position']/724, df2['Thrust sigma']/df2['Thrust_mean'], 'ro--', label = 'Coefficient of Variation')
ax2.plot(df2['Reletive Position'], df2['Thrust sigma']/df2['Thrust_mean'], 'ro--')
ax3.plot(df2['Reletive Position']/724, df2['Thrust sigma'], 'bo--', label = 'Standard Deviation')
#plot standar deviation against position without mean values
ax1.set_ylabel(r'Coefficient of Variation $\frac{\sigma}{\mu}$')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
ax2.set_xlabel('Distance from Rotor (mm)')
ax3.set_ylabel(r'$\sigma$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.grid('both')
ax2.grid(False)
ax3.grid(False)
plt.show()
ax1.legend(bbox_to_anchor=(1,1), loc = 1)
ax3.legend(bbox_to_anchor = (0.7,1), loc = 2)
plt.savefig('Results/Performance Coefficients/TSR4/Thrust Standard Deviation.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, ax3
# %%
#plot My for the three blades with error bars
fig2 = plt.figure(figsize = (60,60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()

eb5 = ax1.errorbar(df2['Reletive Position']/724, df2['My1 mean'], df2['My1 sigma'], label = 'My1', fmt = 'ro', color = 'red', ecolor = 'red', elinewidth=1, capsize=10)
eb5[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
eb1 = ax2.errorbar(df2['Reletive Position'], df2['My1 mean'], df2['My1 sigma'], label = 'My1', fmt = 'ro', color = 'red', ecolor = 'red', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))


eb6 = ax1.errorbar(df2['Reletive Position']/724, df2['My2 mean'], df2['My2 sigma'], label = 'My2' , fmt = 'bo', color = 'black', ecolor = 'black', elinewidth=1, capsize=10)
eb6[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
eb2 = ax2.errorbar(df2['Reletive Position'], df2['My2 mean'], df2['My2 sigma'], label = 'My2' , fmt = 'bo', color = 'black', ecolor = 'black', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))


eb7 = ax1.errorbar(df2['Reletive Position']/724, df2['My3 mean'], df2['My3 sigma'], label = 'My3', fmt = 'go', color = 'green', ecolor = 'green', elinewidth=1, capsize=10)
eb7[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
eb3 = ax2.errorbar(df2['Reletive Position'], df2['My3 mean'], df2['My3 sigma'], label = 'My3', fmt = 'go', color = 'green', ecolor = 'green', elinewidth=1, capsize=10)
eb3[-1][0].set_linestyle('--')


ax1.set_ylabel('Torque N/m')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax1.grid('both')
ax2.grid(False)
plt.savefig('Results/Performance Coefficients/TSR4/My.png', dpi = 600)
plt.close()
del fig2, ax1, ax2, eb5, eb6, eb7, eb1, eb2, eb3


#plot Standard deviation in My for the three blades
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(df2['Reletive Position']/724, df2['My1 sigma'], 'o--',label = 'My1')
ax1.plot(df2['Reletive Position']/724, df2['My2 sigma'], 'o--',label = 'My2')
ax1.plot(df2['Reletive Position']/724, df2['My3 sigma'], 'o--',label = 'My3')


ax2.plot(df2['Reletive Position'], df2['My1 sigma'], 'o--',label = 'My1')
ax2.plot(df2['Reletive Position'], df2['My2 sigma'], 'o--',label = 'My2')
ax2.plot(df2['Reletive Position'], df2['My3 sigma'], 'o--',label = 'My3')

ax1.set_ylabel(r'$\sigma$ N/m')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax1.grid('both')
ax2.grid(False)
plt.savefig('Results/Performance Coefficients/TSR4/My Standard deviation.png', dpi = 600)
plt.close()
del fig2, ax1, ax2

#plot coefficient of variation in My for the three blades
fig2 = plt.figure(figsize = (60, 60))
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(df2['Reletive Position']/724, -df2['My1 sigma']/df2['My1 mean'], 'o--',label = 'My1')
ax1.plot(df2['Reletive Position']/724, -df2['My2 sigma']/df2['My2 mean'], 'o--',label = 'My2')
ax1.plot(df2['Reletive Position']/724, -df2['My3 sigma']/df2['My3 mean'], 'o--',label = 'My3')


ax2.plot(df2['Reletive Position'], -df2['My1 sigma']/df2['My1 mean'], 'o--',label = 'My1')
ax2.plot(df2['Reletive Position'], -df2['My2 sigma']/df2['My2 mean'], 'o--',label = 'My2')
ax2.plot(df2['Reletive Position'], -df2['My3 sigma']/df2['My3 mean'], 'o--',label = 'My3')

ax1.set_ylabel(r'Coefficient of Variation $\frac{\sigma}{\mu}$')
ax2.set_xlabel('Position (mm) from Rotor')
ax1.set_xlabel(r'Normalised Mast Position $\frac{Distance}{Diameter}$')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.legend()
ax1.grid('both')
ax2.grid(False)
plt.savefig('Results/Performance Coefficients/TSR4/My Coefficient of Variation.png', dpi = 600)
plt.close()
