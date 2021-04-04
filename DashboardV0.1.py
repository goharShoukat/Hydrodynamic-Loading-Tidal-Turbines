#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 19:48:52 2021

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
        #window layout
        mainLayout = QtWidgets.QGridLayout()
        #File Name and loading in sublayout
        subLayout = QtWidgets.QGridLayout()
        #signal to load and plotting butons in sublayout2
        subLayout2 = QtWidgets.QGridLayout()
        subLayout3 = QtWidgets.QGridLayout()
        #Introduce widgets here
        
        
        #sublayout widgets
        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setText('File Name')
        self.file_display = QtWidgets.QLineEdit(self)
        self.file_btn = QtWidgets.QPushButton('...', self)
        self.load_btn = QtWidgets.QPushButton('Load Data', self)
        
        #sublayout2 widgets
        self.signal_label = QtWidgets.QLabel(self)
        self.signal_label.setText('Signal')
        self.combo_box = QComboBox(self) 
        self.combo_box.addItems(['Thrust', 'Torque', 'Fx1', 'Fy1', 'Mx1', 'My1', 'Mz1', 'Fx2', 'Fy2', 'Mx2', 'My2', 'Mz2', 'Fx3', 'Fy3', 'Mx3', 'My3', 'Mz3', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        self.plot_btn = QtWidgets.QPushButton('Plot', self)
        #self.plot_btn.pressed.connect() 
        
        #add the input options for fft windowing, run time, sampling frequency
        #Total Run Time
        self.time_label = QtWidgets.QLabel(self)
        self.time_label.setText('Total Run Time')
        self.time_input = QtWidgets.QLineEdit(self)
        self.time_input.setText(str(360.0))
        
        #Sampling Frequency
        self.sampl_freq = QtWidgets.QLabel(self)
        self.sampl_freq.setText('Sampling Frequency')
        self.sampl_freq.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sampl_freq_input = QtWidgets.QLineEdit(self)
        self.sampl_freq_input.setText(str(256))
        
        
        #Set up bins for fft
        self.fft_label = QtWidgets.QLabel(self)
        self.fft_label.setText('Bins for FFT')
        self.fft_input = QtWidgets.QLineEdit(self)
        self.fft_input.setText('Default')
        self.fft_checkbox = QtWidgets.QCheckBox('Normalize FFT', self)
        
        #Provide input for bins for histograms
        self.bin_label = QtWidgets.QLabel(self)
        self.bin_label.setText('Histogram Bins')
        self.bin_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.bin_input = QtWidgets.QLineEdit(self)
        self.bin_input.setText('50')
        
        #horizontally stack file selection, time and sampling frequency
        subLayout.addWidget(self.file_label, 0, 0)
        subLayout.addWidget(self.file_display, 0, 1)
        subLayout.addWidget(self.file_btn, 0, 2)
        subLayout.addWidget(self.load_btn, 0, 3)        

        subLayout3.addWidget(self.time_label, 0, 0)
        subLayout3.addWidget(self.time_input, 0, 1)
        subLayout3.addWidget(self.sampl_freq, 0, 2)
        subLayout3.addWidget(self.sampl_freq_input, 0, 3)
        subLayout3.addWidget(self.signal_label, 1, 0)
        subLayout3.addWidget(self.combo_box, 1, 1)

        subLayout3.addWidget(self.bin_label, 1, 2)
        subLayout3.addWidget(self.bin_input, 1, 3)
        subLayout3.addWidget(self.fft_checkbox, 1, 4)
        subLayout3.addWidget(self.plot_btn, 1, 5)
        
        
        subLayout3.addWidget(self.fft_label, 0, 4)
        subLayout3.addWidget(self.fft_input, 0, 5)

        #add figures
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
        
        mainLayout.addLayout(subLayout, 0, 0)
        mainLayout.addLayout(subLayout2, 1, 0)
        mainLayout.addLayout(subLayout3, 0, 1)
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
        
      

        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())