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


path = 'Cp_Ct/'
df = pd.read_csv(path+'Experiment_Summary.csv')

#dataframe with the information regarding TSR 4 only
df2 = df[(df['TSR'] == '4,00') & (df['Velocity'] == '1')]
df2 = df2.reset_index(drop = True)
#important to convert the comma to decimal for python to interpret it as a floating point
#convert the strings to floating point to sort the column for plotting
df2['Reletive Position'] = df2['Reletive Position'].str.replace(',','.').astype(float)
df2 = df2.drop([0, 1, 2, 15])
df2 = df2.sort_values('Reletive Position')
#plot Reletive Position against Cp
error_Cp = df2['Cp sigma']

plt.errorbar(df2['Reletive Position'], df2['Cp mean'], error_Cp)
plt.show()
plt.ylabel(r'$C_p$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.savefig('Results/Performance Coefficients/TSR4/Cp.png')
plt.close()

#Plot Ct
plt.errorbar(df2['Reletive Position'], df2['Ct mean'], df2['Ct sigma'])
plt.ylabel(r'$C_t$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.savefig('Results/Performance Coefficients/TSR4/Ct.png')
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Cp sigma'], label = '$C_p$')
plt.plot(df2['Reletive Position'], df2['Ct sigma'], label = '$C_t$')
plt.ylabel(r'$\sigma$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.savefig('Results/Performance Coefficients/TSR4/Cp Ct Standard Deviation.png')
plt.close()


#plot torque against 
plt.errorbar(df2['Reletive Position'], df2['Torque_mean'], df2['Torque sigma'])
plt.ylabel('Torque (N/m)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.savefig('Results/Performance Coefficients/TSR4/torque.png')
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Torque sigma'])
plt.ylabel(r'$\sigma$')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.savefig('Results/Performance Coefficients/TSR4/Torque Standard Deviation.png')
plt.close()

#plot thrust against  
plt.errorbar(df2['Reletive Position'], df2['Thrust_mean'], df2['Thrust sigma'])
plt.ylabel('Thrust (N)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.savefig('Results/Performance Coefficients/TSR4/thrust.png')
plt.close()

#plot standar deviation against position without mean values
plt.plot(df2['Reletive Position'], df2['Thrust sigma'])
plt.ylabel(r'$\sigma$ (N)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.savefig('Results/Performance Coefficients/TSR4/Thrust Standard Deviation.png')
plt.close()


#plot My for the three blades with error bars
plt.errorbar(df2['Reletive Position'], df2['My1 mean'], df2['My1 sigma'], label = 'My1')
plt.errorbar(df2['Reletive Position'], df2['My2 mean'], df2['My2 sigma'], label = 'My2')
plt.errorbar(df2['Reletive Position'], df2['My3 mean'], df2['My3 sigma'], label = 'My3')
plt.ylabel('N/m')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.savefig('Results/Performance Coefficients/TSR4/My.png')
plt.close()

#plot Standard deviation in My for the three blades
plt.plot(df2['Reletive Position'], df2['My1 sigma'], label = 'My1')
plt.plot(df2['Reletive Position'], df2['My2 sigma'], label = 'My2')
plt.plot(df2['Reletive Position'], df2['My3 sigma'], label = 'My3')
plt.ylabel(r'$\sigma$ (N/m)')
plt.xlabel('Position (mm) from Rotor')
plt.title('TSR 4.0, Vel = 1 m/s')
plt.legend()
plt.savefig('Results/Performance Coefficients/TSR4/My Standard deviation.png')
plt.close()