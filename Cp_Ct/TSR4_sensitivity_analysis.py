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



#plot Reletive Position against Cp
error_Cp = df2['Cp sigma']
fig2 = plt.figure()
ax1 = fig2.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Cp mean'], error_Cp, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--')
eb2 = ax2.errorbar(df2['Reletive Position'], df2['Cp mean'], error_Cp, fmt = 'o',  color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--')
ax1.set_xticks(np.linspace(np.min(df2['Reletive Position']/724), np.max(df2['Reletive Position']/724), 10))
ax1.set_ylabel(r'$C_p$')

plt.show()


a, b = 9, 10
print(a & b)#line 1
print(a and b)#line 2

'''

#plot Cp
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
eb1 = ax1.errorbar(df2['Reletive Position']/724, df2['Cp mean'], error_Cp, fmt = 'o', color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb1[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines
ax2.set_xticks(df2['Reletive Position'])
ax1.set_ylabel(r'$C_p$')
ax1.set_xlabel('Normalised Distance from Rotor $\frac{Dist}{Dia}$')
ax2.set_xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
ax1.grid(True)
ax2.grid(False)
plt.show()
plt.savefig('Results/Performance Coefficients/TSR4/Cp.png', dpi = 1200)
plt.close()
'''
#Plot Ct
eb2 = plt.errorbar(df2['Reletive Position'], df2['Ct mean'], df2['Ct sigma'], fmt = 'o', color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb2[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines
plt.ylabel(r'$C_t$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/Ct.png', dpi = 1200)
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Cp sigma'], 'o--', label = '$C_p$')
plt.plot(df2['Reletive Position'], df2['Ct sigma'], 'o--', label = '$C_t$')
plt.ylabel(r'$\sigma$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/Cp Ct Standard Deviation.png', dpi = 1200)
plt.close()


#plot torque against 
eb3 = plt.errorbar(df2['Reletive Position'], df2['Torque_mean'], df2['Torque sigma'], fmt = 'o', color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb3[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines
plt.ylabel('Torque (N/m)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/torque.png', dpi = 1200)
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Torque sigma'], 'o--')
plt.ylabel(r'$\sigma$ (N/m)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/Torque Standard Deviation.png', dpi = 1200)
plt.close()

#plot thrust against  
eb4 = plt.errorbar(df2['Reletive Position'], df2['Thrust_mean'], df2['Thrust sigma'], fmt = 'o', color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb4[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines)
plt.ylabel('Thrust (N)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/thrust.png', dpi = 1200)
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Thrust sigma'], 'o--')
plt.ylabel(r'$\sigma$ (N)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/Thrust Standard Deviation.png', dpi = 1200)
plt.close()


#plot My for the three blades with error bars
eb5 = plt.errorbar(df2['Reletive Position'], df2['My1 mean'], df2['My1 sigma'], label = 'My1', fmt = 'ro', color = 'red', ecolor = 'gray', elinewidth=1, capsize=10)
eb5[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
eb6 = plt.errorbar(df2['Reletive Position'], df2['My2 mean'], df2['My2 sigma'], label = 'My2' , fmt = 'bo', color = 'black', ecolor = 'gray', elinewidth=1, capsize=10)
eb6[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
eb7 = plt.errorbar(df2['Reletive Position'], df2['My3 mean'], df2['My3 sigma'], label = 'My3', fmt = 'go', color = 'green', ecolor = 'gray', elinewidth=1, capsize=10)
eb7[-1][0].set_linestyle('--') #eb1[-1][0] is the LineCollection objects of the errorbar lines))
plt.ylabel('Torque N/m')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/My.png', dpi = 1200)
plt.close()

#plot Standard deviation in My for the three blades
plt.plot(df2['Reletive Position'], df2['My1 sigma'], 'o--',label = 'My1')
plt.plot(df2['Reletive Position'], df2['My2 sigma'], 'o--',label = 'My2')
plt.plot(df2['Reletive Position'], df2['My3 sigma'], 'o--',label = 'My3')
plt.ylabel(r'$\sigma$ (N/m)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.grid()
plt.savefig('Results/Performance Coefficients/TSR4/My Standard deviation.png', dpi = 1200)
plt.close()