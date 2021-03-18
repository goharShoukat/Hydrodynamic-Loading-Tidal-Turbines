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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QDialog, QComboBox
import os
import sys
from pathlib import Path
import data_import_func
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
       # self.signal = self.l2_cb.currentText()
        

        self.plot_b2 = QtWidgets.QPushButton('Plot', self)
       # self.plot_b2.clicked.connect(self.plot)
        self.plot_b2.pressed.connect(self.find) 

        figure1 = Figure()
        figure2 = Figure()
        figure3 = Figure()
        figure4 = Figure()
        canvas1 = FigureCanvas(figure1)
        canvas2 = FigureCanvas(figure2)
        canvas3 = FigureCanvas(figure3)
        canvas4 = FigureCanvas(figure4)
        self.ax1 = figure1.add_subplot(111)
        self.ax2 = figure2.add_subplot(111)
        self.ax3 = figure3.add_subplot(111)
        self.ax4 = figure4.add_subplot(111)
        
        
        toolbar1 = NavigationToolbar(canvas1, self)
        toolbar2 = NavigationToolbar(canvas2, self)
        toolbar3 = NavigationToolbar(canvas3, self)
        toolbar4 = NavigationToolbar(canvas4, self)
        
        mainLayout.addWidget(self.l1, 0, 0)
        mainLayout.addWidget(self.l1_input, 0, 1)
        mainLayout.addWidget(self.l1_b1, 0,2)
        mainLayout.addWidget(self.load_b3, 0, 3)
        mainLayout.addWidget(self.l2, 1,0)
        mainLayout.addWidget(self.combo_box, 1, 1)
        mainLayout.addWidget(self.plot_b2, 1, 2)
        mainLayout.addWidget(toolbar1,2,0)
        mainLayout.addWidget(toolbar2,2,1)
        mainLayout.addWidget(toolbar3,4,0)
        mainLayout.addWidget(toolbar4,4,1)
        mainLayout.addWidget(canvas1,3,0)
        mainLayout.addWidget(canvas2,3,1)
        mainLayout.addWidget(canvas3,5,0)
        mainLayout.addWidget(canvas4,5,1)
        
        
  
        self.setLayout(mainLayout)
        self.setWindowTitle("Dashboard")
        
    def find(self): 
  
        # finding the content of current item in combo box 
        self.content = self.combo_box.currentText() 
        self.l1_input.setText(self.content)
    
    def openFile(self):
        
        self.filename, _ = QFileDialog.getOpenFileName(self, 'File')
        #self.l1_input.setText(str(self.filename))
        return self.filename

        
    def readFile(self):
        #self.Fx, self.Fx1, self.Fx2, self.Fx3, self.Thrust = 
        self.df = data_import_func.access_file(self.filename)
        
    def plot(self):
        self.l1_input.setText(str(self.signal))
        '''if self.signal == 'Fx':
            self.ax1.plot(self.df['Fx1'])
        
        else:
            self.ax1.plot(self.df['Fx1'])'''
        
    
      
        

        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
