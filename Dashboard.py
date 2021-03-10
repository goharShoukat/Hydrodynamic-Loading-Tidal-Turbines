#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:38:36 2021

@author: goharshoukat
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import numpy as np
class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax1 = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)
        
        t = np.arange(0, 2, 0.01)
        s = 1 + np.sin(2*np.pi*t)
        self.ax1.plot(t, s)
        self.ax1.grid
        
        
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 800)
        
        chart = Canvas(self)
        
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
    
'''
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        title = 'Statistical Data Represenation'
        top = 400
        left = 400
        width = 900
        height = 500
        
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.MyUI()
        
    def MyUI(self):
        canvas = Canvas(self, 8, 4)
        canvas.move(0,0)
        button = QPushButton('Run', self)
        button.move(100, 450)
        
        button2 = QPushButton('Run', self)
        button2.move(250, 450)
        
        

class Canvas(FigureCanvas):
    def __init__(self, parent, width = 5, height = 5, dpi = 100):
        fig=  Figure(figsize = (width, height), dpi = dpi)
        self.axes = fig.add_subplot(111)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()
        
    def plot(self):
        x = np.array([5, 1, 2])
        labels = ['Applies', 'bens', 'C']
        ax = self.figure.add_subplot(111)
        ax.pie(x, labels = labels)
        
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
'''
'''
import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
        '''
       

'''
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('pyqtgraph example: GraphicsLayout')
view.resize(800,600)

## Title at top
text = """
This example demonstrates the use of GraphicsLayout to arrange items in a grid.<br>
The items added to the layout must be subclasses of QGraphicsWidget (this includes <br>
PlotItem, ViewBox, LabelItem, and GrphicsLayout itself).
"""
l.addLabel(text, col=1, colspan=4)
l.nextRow()

## Put vertical label on left side
l.addLabel('Long Vertical Label', angle=-90, rowspan=3)

## Add 3 plots into the first row (automatic position)
p1 = l.addPlot(title="Plot 1")
p2 = l.addPlot(title="Plot 2")
vb = l.addViewBox(lockAspect=True)
img = pg.ImageItem(np.random.normal(size=(100,100)))
vb.addItem(img)
vb.autoRange()


## Add a sub-layout into the second row (automatic position)
## The added item should avoid the first column, which is already filled
l.nextRow()
l2 = l.addLayout(colspan=3, border=(50,0,0))
l2.setContentsMargins(10, 10, 10, 10)
l2.addLabel("Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=3)
l2.nextRow()
l2.addLabel('Vertical Axis Label', angle=-90, rowspan=2)
p21 = l2.addPlot()
p22 = l2.addPlot()
l2.nextRow()
p23 = l2.addPlot()
p24 = l2.addPlot()
l2.nextRow()
l2.addLabel("HorizontalAxisLabel", col=1, colspan=2)

## hide axes on some plots
p21.hideAxis('bottom')
p22.hideAxis('bottom')
p22.hideAxis('left')
p24.hideAxis('left')
p21.hideButtons()
p22.hideButtons()
p23.hideButtons()
p24.hideButtons()


## Add 2 more plots into the third row (manual position)
p4 = l.addPlot(row=3, col=1)
p5 = l.addPlot(row=3, col=2, colspan=2)

## show some content in the plots
p1.plot([1,3,2,4,3,5])
p2.plot([1,3,2,4,3,5])
p4.plot([1,3,2,4,3,5])
p5.plot([1,3,2,4,3,5])



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        '''