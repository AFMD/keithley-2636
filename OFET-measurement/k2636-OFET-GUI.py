#!/usr/bin/env python3
#coding:utf-8

"""
  Author:  Ross
  Purpose: Qt5 GUI for making OFET measurements with a Keithley 2636
  Created: 14/05/17
"""

import sys
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, Qt
from PyQt5.QtWidgets import (QMainWindow, QDockWidget, QWidget, QDesktopWidget, QApplication,
                             QGridLayout, QPushButton, QAction, qApp,QMenu,
                             QVBoxLayout, QSizePolicy, QMessageBox, QButtonGroup)

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as mplToolbar
import matplotlib.style as style
from matplotlib.figure import Figure


class ofet_GUI(QMainWindow):
    '''This is the main window class for the GUI'''
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        
        # Add central widget
        self.mainWidget = mplWidget()
        self.setCentralWidget(self.mainWidget)
        
        ## Add dock widgets
        # Keithley dock widget
        self.buttonWidget = buttonWidget()
        self.dockWidget1 = QDockWidget('Keithley Control')
        self.dockWidget1.setWidget(self.buttonWidget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget1)
        # Matplotlib control widget
        self.dockWidget2 = QDockWidget('Plotting controls')
        self.dockWidget2.setWidget(mplToolbar(self.mainWidget, self))
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget2)
        
              
        # Menu bar setup
        exitAction = QAction('&Exit', self) 
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)           
        
        # Status bar setup
        self.statusbar = self.statusBar() 
        self.buttonWidget.statusUpdate[str].connect(self.statusbar.showMessage)
        
        # Window setup
        self.resize(800, 600)
        self.centre()
        self.setWindowTitle('K2636 - OFET Measurements')
        self.show()
        

    def centre(self):
        '''Find screen size and place in centre'''
    
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)    
        
        
class buttonWidget(QWidget):
    """ This is the main buton widget """

    # Define signals to be emitted from widget
    statusUpdate = pyqtSignal(str)
    ivSignal = pyqtSignal()
    outputSignal = pyqtSignal()
    transferSignal = pyqtSignal() 

    def __init__(self):
        super().__init__()
        self.initWidget()
        
    def initWidget(self):
        
        # Set widget layout
        grid = QGridLayout()
        self.setLayout(grid)
                
        # Push button setup
        ivBtn = QPushButton('IV Sweep')
        grid.addWidget(ivBtn, 1, 1)
        ivBtn.clicked.connect(self.ivSweep)
        
        outputBtn = QPushButton('Output Sweep')
        grid.addWidget(outputBtn, 1, 2)       
        outputBtn.clicked.connect(self.outputSweep)  
        
        transferBtn = QPushButton('Transfer Sweep')
        grid.addWidget(transferBtn, 1, 3)       
        transferBtn.clicked.connect(self.transferSweep)           
    
    
    def ivSweep(self, event):
        self.statusUpdate.emit('Performing IV Sweep.')
        self.ivSignal.emit()
        
    def outputSweep(self, event):
        self.statusUpdate.emit('Performing Output Sweep.')
        self.outputSignal.emit()
        
    def transferSweep(self, event):
        self.statusUpdate.emit('Performing Transfer Sweep.') 
        self.transferSignal.emit()
                
                
class mplWidget(FigureCanvas):
    """ Widget for matplotlib figure """
    
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        self.initWidget()
        
    def initWidget(self, parent = None, width = 5, height = 4, dpi = 100):
        
        style.use('ggplot')
        #fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2, 2, figsize=(20, 10), dpi= 80, facecolor='w', edgecolor='k')
        
        #ax1.set_title('IV Sweep')
        #ax1.set_xlabel('Channel Voltage [V]')
        #ax1.set_ylabel('Channel Current [A]')        
        #ax2.set_title('Output Curves')
        #ax2.set_xlabel('Channel Voltage [V]')
        #ax2.set_ylabel('Channel Current [A]')        
        #ax3.set_title('Transfer Curve')
        #ax3.set_xlabel('Gate Voltage [V]')
        #ax3.set_ylabel('Channel Current [A]')        
        #ax4.set_title('Gate Leakage')
        #ax4.set_xlabel('Gate Voltage [V]')
        #ax4.set_ylabel('Gate Leakage [A]')
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)        
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
    
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)           
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = ofet_GUI()
    sys.exit(app.exec_())