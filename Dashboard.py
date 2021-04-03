#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:38:36 2021

@author: goharshoukat
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from PyQt5.QtGui import *
#from PyQt5.QtWidgets import QFileDialog, QDialog, QComboBox
from PyQt5.QtWidgets import *
import os
import sys
from pathlib import Path
import data_import_func
from scipy.stats import norm
import matplotlib.pyplot as plt

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 1000, 1000)
        mainLayout = QtWidgets.QGridLayout()
        
   
        self.l1 = QtWidgets.QLabel(self)
        self.l1.setText('File')

        self.l1_input = QtWidgets.QLineEdit(self)

        self.l1_b1 = QtWidgets.QPushButton('...', self)

        self.directory = self.l1_b1.clicked.connect(self.openFile)
        self.load_b3 = QtWidgets.QPushButton('Load Data', self)
        self.load_b3.clicked.connect(self.readFile)

         
        self.l2 = QtWidgets.QLabel(self)
        self.l2.setText('Signal')
        self.combo_box = QComboBox(self) 
        self.combo_box.addItems(['Thrust', 'Torque', 'Fx1', 'Fy1', 'Mx1', 'My1', 'Mz1', 'Fx2', 'Fy2', 'Mx2', 'My2', 'Mz2', 'Fx3', 'Fy3', 'Mx3', 'My3', 'Mz3', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        
        

        self.plot_b2 = QtWidgets.QPushButton('Plot', self)
        self.plot_b2.pressed.connect(self.plot) 

#display statistical information about the signal
        self.l3 = QtWidgets.QLabel(self)
        self.l3.setText('Average of Time Series')
        self.l3_output = QtWidgets.QLineEdit(self)
        
        self.l4 = QtWidgets.QLabel(self)
        self.l4.setText('Std of Time Series / Normalised Std')
        self.l4_output = QtWidgets.QLineEdit(self)
        
        self.l5 = QtWidgets.QLabel(self)
        self.l5.setText('Max of Time Series / Normalised Max')
        self.l5_output = QtWidgets.QLineEdit(self)
        
        self.l6 = QtWidgets.QLabel(self)
        self.l6.setText('Min of Time Series / Normalised Min')
        self.l6_output = QtWidgets.QLineEdit(self)
        
#add the input options for fft windowing, run time, sampling frequency
#Total Run Time
        self.l7 = QtWidgets.QLabel(self)
        self.l7.setText('Total Run Time')
        self.l7_input = QtWidgets.QLineEdit(self)
        self.l7_input.setText(str(360.0))
#Sampling Frequency
        self.l8 = QtWidgets.QLabel(self)
        self.l8.setText('Sampling Frequency')
        self.l8_input = QtWidgets.QLineEdit(self)
        self.l8_input.setText(str(256))
        
#provide option for bins for fft
        #self.checkbox = QtWidgets.QCheckBox('FFT Customization', self)
        #self.checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)        
        self.l9 = QtWidgets.QLabel(self)
        self.l9.setText('Bins for FFT')
        self.l9_input = QtWidgets.QLineEdit(self)
        self.l9_input.setText('Default')
        self.l10_checkbox = QtWidgets.QCheckBox('Normalize FFT', self)
        
#Provide input for bins for histograms
        self.l11 = QtWidgets.QLabel(self)
        self.l11.setText('Bins for Histogram')
        self.l11_input = QtWidgets.QLineEdit(self)
        self.l11_input.setText('50')
        
    

       
        


        figure1 = Figure()
        figure2 = Figure()
        figure3 = Figure()
        figure4 = Figure()
        self.canvas1 = FigureCanvas(figure1)
        self.canvas2 = FigureCanvas(figure2)
        self.canvas3 = FigureCanvas(figure3)
        self.canvas4 = FigureCanvas(figure4)
        self.ax1 = figure1.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax2 = figure2.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax3 = figure3.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax4 = figure4.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75], projection='polar')
        
        
        toolbar1 = NavigationToolbar(self.canvas1, self)
        toolbar2 = NavigationToolbar(self.canvas2, self)
        toolbar3 = NavigationToolbar(self.canvas3, self)
        toolbar4 = NavigationToolbar(self.canvas4, self)
        
        mainLayout.addWidget(self.l1, 0, 0)
        mainLayout.addWidget(self.l1_input, 0, 1)
        mainLayout.addWidget(self.l1_b1, 0,2)
        mainLayout.addWidget(self.load_b3, 0, 7)
        mainLayout.addWidget(self.l2, 1,0)
        mainLayout.addWidget(self.combo_box, 1, 1)
        mainLayout.addWidget(self.plot_b2, 1, 2)
        mainLayout.addWidget(self.l3, 2, 2)
        mainLayout.addWidget(self.l3_output, 2, 3)
        mainLayout.addWidget(self.l4, 3,2)
        mainLayout.addWidget(self.l4_output,3,3)
        mainLayout.addWidget(self.l5, 4,2)
        mainLayout.addWidget(self.l5_output,4, 3)
        mainLayout.addWidget(self.l6, 5,2)
        mainLayout.addWidget(self.l6_output,5, 3)
        
        mainLayout.addWidget(self.l7, 0,3)
        mainLayout.addWidget(self.l7_input,0, 4)
        mainLayout.addWidget(self.l8, 0, 5)
        mainLayout.addWidget(self.l8_input, 0, 6)

        mainLayout.addWidget(self.l9, 1,4)
        mainLayout.addWidget(self.l9_input, 1,5)
 
        mainLayout.addWidget(self.l10_checkbox, 1,6)
        mainLayout.addWidget(self.l11, 2, 6)
        mainLayout.addWidget(self.l11_input, 2, 7)
        
        
        mainLayout.addWidget(toolbar1,2,0)
        mainLayout.addWidget(toolbar2,2,1)
        mainLayout.addWidget(toolbar3,4,0)
        mainLayout.addWidget(toolbar4,4,1)
        mainLayout.addWidget(self.canvas1,3,0)
        mainLayout.addWidget(self.canvas2,3,1)
        mainLayout.addWidget(self.canvas3,5,0)
        mainLayout.addWidget(self.canvas4,5,1)
        
        
  
        self.setLayout(mainLayout)
        self.setWindowTitle("Dashboard")


        
    
    
    def openFile(self):
        

        self.filename, _ = QFileDialog.getOpenFileName(self, 'File')
        self.l1_input.setText(str(self.filename))

        return self.filename

        
    def readFile(self):
        self.l7_get_text = float(self.l7_input.text())
        self.l8_get_text = float(self.l8_input.text())
       
        
        self.df = data_import_func.access_file(self.filename, self.l7_get_text, self.l8_get_text)
        
    def plot(self):
        #Figure 1 is used to plot the time series. 
        
        self.ax1.clear()
        self.content = self.combo_box.currentText() 
        std_val, mean_val, max_val, min_val = data_import_func.stats(self.df[self.content])
        self.l3_output.setText('%.5s' % str(mean_val))
        #Add Normalisation to the statistical parameters
        self.l4_output.setText('%.5s' % str(std_val) + '/' + '%.4s' % str(std_val/mean_val))
        self.l5_output.setText('%.5s' % str(max_val) + '/' + '%.4s' % str(max_val/mean_val))
        self.l6_output.setText('%.5s' % str(min_val) + '/' + '%.4s' % str(min_val/mean_val))
        mean_array = [mean_val] * len(self.df[self.content])
        self.ax1.plot(self.df[self.content], label = 'Data')
        self.ax1.plot(self.df.index,mean_array, label = 'Mean', linestyle = '--')
        self.ax1.set_ylabel('Force [N]')
        self.ax1.set_xlabel('Time [s]')
        self.ax1.set_title('Time Signal')
        self.ax1.grid()
        self.ax1.legend()
        self.canvas1.draw()
    
        #Figure 2 will be used to plot the fft
        #read the bins provided for the fft operation
        if self.l9_input.text() == 'Default':
            self.l9_get_text = 'Default'
        else:
            self.l9_get_text = float(self.l9_input.text())
       
        #allow for normalisation using the checkbox 
        spec, freq = data_import_func.spectral_analysis(self.df,self.content, self.l7_get_text, self.l8_get_text, self.l9_get_text)
        self.ax2.clear()
        
        if self.l10_checkbox.isChecked() == True:
            rotor_freq = data_import_func.rotor_freq(self.df['RPM'])
            freq = freq/rotor_freq            
            self.ax2.loglog(freq[1:int(len(freq)/2)], spec[1:])
            self.ax2.set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')
            self.ax2.set_title('Normalised FFT')
           
        else:
            self.ax2.loglog(freq[1:int(len(freq)/2)], spec[1:])
            self.ax2.set_xlabel('Frequency [s]')
            self.ax2.set_title('FFT')
            
        self.ax2.set_ylabel('Force [N]')
        self.ax2.grid(True, which = 'both', ls = '--')
        self.canvas2.draw()
        
        #read the bins for the histogram first
        self.l11_get_text = int(self.l11_input.text())
        #Figure 3 will be used to plot a normal distribution of normalised loads
        self.ax3.clear()
        self.ax3.hist(self.df[self.content], bins = self.l11_get_text, density=True)
        self.ax3.set_xlabel('Force [N]')
        self.ax3.set_ylabel('PDF')
        sorted_array = self.df.sort_values(by=self.content)[self.content]
        self.ax3.plot(sorted_array, norm.pdf(sorted_array, mean_val, std_val))
        self.ax3.set_title('Probability density Function')
        self.ax3.grid()
        self.canvas3.draw()
        
        #Plot the polar chart with 
        #pass values to the function angle_turbine
        t = self.df.index.to_numpy()
        Fy1 = self.df['Fy1'].to_numpy()
        Fy2 = self.df['Fy2'].to_numpy()
        Fy3 = self.df['Fy3'].to_numpy()
        fr= data_import_func.rotor_freq(self.df['RPM'])
        self.theta = data_import_func.angle_turbine(t, Fy1, Fy2, Fy3, fr)
        self.ax4.clear()
        #half the samples are plotted to avoid clutter
        self.ax4.scatter(self.theta[0:(int(len(self.theta)/2))], self.df[self.content][0:(int(self.l7_get_text/2))], s = 0.01, alpha = 0.75)
        self.canvas4.draw()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
