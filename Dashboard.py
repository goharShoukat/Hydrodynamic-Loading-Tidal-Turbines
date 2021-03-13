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
from PyQt5.QtWidgets import QFileDialog, QDialog
import os
import sys
from pathlib import Path

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        mainLayout = QtWidgets.QGridLayout()
        self.l1 = QtWidgets.QLabel(self)
        self.l1.setText('File Name')
        mainLayout.addWidget(self.l1, 0,0)
        self.l1_input = QtWidgets.QLineEdit(self)
        mainLayout.addWidget(self.l1_input, 0,1)
        self.l1_b1 = QtWidgets.QPushButton('...')
        mainLayout.addWidget(self.l1_b1, 0,2)
        self.directory = self.l1_b1.clicked.connect(self.openFile)
       
        self.l2 = QtWidgets.QLabel(self)
        self.l2.setText('Signal')
        mainLayout.addWidget(self.l2, 1,0)
        self.l2_input = QtWidgets.QLineEdit(self)
        mainLayout.addWidget(self.l2_input)

        
        self.setLayout(mainLayout)
    
    def openFile(self):
        
        self.filename, _ = QFileDialog.getOpenFileName(self, 'File')
        #print(self.filename)
        self.l1_input.setText(str(self.filename))
        return self.filename
        

        
                #self.textedit.setText(data)
       # QFileDialog.getOpenFileName(self, 'Select file')  # For file.


      
    
       
        '''
        figure1 = Figure()
        figure2 = Figure()
        figure3 = Figure()
        figure4 = Figure()
        canvas1 = FigureCanvas(figure1)
        canvas2 = FigureCanvas(figure2)
        canvas3 = FigureCanvas(figure3)
        canvas4 = FigureCanvas(figure4)
        ax1 = figure1.add_subplot(111)
        ax2 = figure2.add_subplot(111)
        ax3 = figure3.add_subplot(111)
        ax4 = figure4.add_subplot(111)
        toolbar1 = NavigationToolbar(canvas1, self)
        toolbar2 = NavigationToolbar(canvas2, self)
        toolbar3 = NavigationToolbar(canvas3, self)
        toolbar4 = NavigationToolbar(canvas4, self)

        
        mainLayout.addWidget(_audio_file, 0,0)
      #  mainLayout.addWidget(toolbar1,0,0)
        mainLayout.addWidget(toolbar2,0,1)
        mainLayout.addWidget(toolbar3,2,0)
        mainLayout.addWidget(toolbar4,2,1)
        mainLayout.addWidget(canvas1,1,0)
        mainLayout.addWidget(canvas2,1,1)
        mainLayout.addWidget(canvas3,3,0)
        mainLayout.addWidget(canvas4,3,1)
        
        self.setWindowTitle("Flow Layout")
        '''

        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
