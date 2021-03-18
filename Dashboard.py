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
from PyQt5.QtWidgets import QFileDialog, QDialog, QComboBox
import os
import sys
from pathlib import Path
import data_import_func
from scipy.stats import norm

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 1000, 800)
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
        self.combo_box.addItems(['Fx', 'Fx1', 'Fx2', 'Fx3', 'Thrust'])

        

        self.plot_b2 = QtWidgets.QPushButton('Plot', self)
        self.plot_b2.pressed.connect(self.plot) 

#display statistical information about the signal
        self.l3 = QtWidgets.QLabel(self)
        self.l3.setText('Average of Time Series')
        self.l3_output = QtWidgets.QLineEdit(self)
        
        self.l4 = QtWidgets.QLabel(self)
        self.l4.setText('Std of Time Series')
        self.l4_output = QtWidgets.QLineEdit(self)
        
        self.l5 = QtWidgets.QLabel(self)
        self.l5.setText('Max of Time Series')
        self.l5_output = QtWidgets.QLineEdit(self)
        
        self.l6 = QtWidgets.QLabel(self)
        self.l6.setText('Min of Time Series')
        self.l6_output = QtWidgets.QLineEdit(self)
        


        figure1 = Figure()
        figure2 = Figure()
        figure3 = Figure()
        figure4 = Figure()
        self.canvas1 = FigureCanvas(figure1)
        self.canvas2 = FigureCanvas(figure2)
        self.canvas3 = FigureCanvas(figure3)
        self.canvas4 = FigureCanvas(figure4)
        self.ax1 = figure1.add_subplot(111)
        self.ax2 = figure2.add_subplot(111)
        self.ax3 = figure3.add_subplot(111)
        self.ax4 = figure4.add_subplot(111)
        
        
        toolbar1 = NavigationToolbar(self.canvas1, self)
        toolbar2 = NavigationToolbar(self.canvas2, self)
        toolbar3 = NavigationToolbar(self.canvas3, self)
        toolbar4 = NavigationToolbar(self.canvas4, self)
        
        mainLayout.addWidget(self.l1, 0, 0)
        mainLayout.addWidget(self.l1_input, 0, 1)
        mainLayout.addWidget(self.l1_b1, 0,2)
        mainLayout.addWidget(self.load_b3, 0, 3)
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
        self.df = data_import_func.access_file(self.filename)
        
    def plot(self):
        #Figure 1 is used to plot the time series. 
        
        self.ax1.clear()
        self.content = self.combo_box.currentText() 
        std_val, mean_val, max_val, min_val = data_import_func.stats(self.df[self.content])
        self.l3_output.setText('%.6s' % str(mean_val))
        self.l4_output.setText('%.6s' % str(std_val))
        self.l5_output.setText('%.6s' % str(max_val))
        self.l6_output.setText('%.6s' % str(min_val))
        mean_array = [mean_val] * len(self.df[self.content])
        self.ax1.plot(self.df[self.content], label = 'Data')
        self.ax1.plot(self.df.index,mean_array, label = 'Mean', linestyle = '--')
        self.ax1.set_ylabel('Force [N]')
        self.ax1.set_xlabel('Time [s]')
        self.ax1.legend()
        self.canvas1.draw()
    
        #Figure 2 will be used to plot the fft
        spec, freq = data_import_func.spectral_analysis(self.df,self.content)
        self.ax2.clear()
        self.ax2.loglog(freq[1:int(len(freq)/2)], spec[1:])
        self.ax2.set_ylabel('Force [N]')
        self.ax2.set_xlabel('Frequency [s]')
        self.canvas2.draw()
        
        #Figure 3 will be used to plot a normal distribution of normalised loads
        self.ax3.clear()
        self.ax3.hist(self.df[self.content], bins = 50, density=True)
        self.ax3.set_xlabel('Force [N]')
        self.ax3.set_ylabel('PDF')
        sorted_array = self.df.sort_values(by=self.content)[self.content]
        self.ax3.plot(sorted_array, norm.pdf(sorted_array, mean_val, std_val))
        self.canvas3.draw()
        

        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
