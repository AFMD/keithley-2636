#!/usr/bin/env python3
#coding:utf-8

"""
  Author:  Ross
  Purpose: Qt5 GUI for making OFET measurements with a Keithley 2636
  Created: 14/05/17
"""

import sys
import fnmatch
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, Qt
from PyQt5.QtWidgets import (QMainWindow, QDockWidget, QWidget, QDesktopWidget, QApplication,
                             QGridLayout, QPushButton,QLabel, QDoubleSpinBox, QAction, qApp,QMenu,
                             QVBoxLayout, QSizePolicy, QMessageBox, QButtonGroup, QTextEdit, QFileDialog)

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as mplToolbar
import matplotlib.style as style
from matplotlib.figure import Figure

import k2636 # Driver for keithley 2636


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
		self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget1)
		# Matplotlib control widget
		self.dockWidget2 = QDockWidget('Plotting controls')
		self.dockWidget2.setWidget(mplToolbar(self.mainWidget, self))
		self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget2)   

		## Menu bar setup
		# Shutdown program
		exitAction = QAction('&Exit', self) 
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		# Load old data
		loadAction = QAction('&Load', self) 
		loadAction.setShortcut('Ctrl+L')
		loadAction.setStatusTip('Load data to be displayed')
		loadAction.triggered.connect(self.showFileOpen)
		# Clear data
		clearAction = QAction('Clear', self)
		clearAction.setShortcut('Ctrl+C')
		clearAction.setStatusTip('Clear data on graph')
		clearAction.triggered.connect(self.mainWidget.clear)
		# Keithley settings popup
		keithleyAction = QAction('Settings', self)
		keithleyAction.setShortcut('Ctrl+K')
		keithleyAction.setStatusTip('Adjust scan parameters')
		keithleyConAction = QAction('Connect', self)
		keithleyConAction.setShortcut('Ctrl+K')
		keithleyConAction.setStatusTip('Reconnect to keithley 2636')        
		keithleyAction.triggered.connect(self.popupKeithleySettings)
		keithleyConAction.triggered.connect(self.popupKeithleyConnection)
		
		# Add items to menu bars
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(loadAction)
		fileMenu.addAction(clearAction)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAction)
		keithleyMenu = menubar.addMenu('&Keithley')        
		keithleyMenu.addAction(keithleyConAction)
		keithleyMenu.addAction(keithleyAction)

		# Status bar setup
		self.statusbar = self.statusBar() 
		self.buttonWidget.statusUpdate[str].connect(self.statusbar.showMessage)

		# Window setup
		self.resize(800, 800)
		self.centre()
		self.setWindowTitle('K2636 - OFET Measurements')
		self.show()


	def centre(self):
		'''Find screen size and place in centre'''

		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width()-size.width())/2, 
	          (screen.height()-size.height())/2)

	def popupKeithleySettings(self):
		self.popupWindow = keithleySettingsWindow()
		
	def popupKeithleyConnection(self):
		self.popupWindow = keithleyConnectionWindow()
		
	def showFileOpen(self):
		'''Pop up for file selection'''
		
		fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/ross/physics/data/transistor/blank-chip-results/23-05-2017')
		if fname[0]:
			df = pd.read_csv(fname[0], '\t')
			if fnmatch.fnmatch(fname[0], '*iv-sweep.csv'):
				self.mainWidget.drawIV(df)
			if fnmatch.fnmatch(fname[0], '*output.csv'):
				self.mainWidget.drawOutput(df)	
			if fnmatch.fnmatch(fname[0], '*transfer.csv'):
				self.mainWidget.drawTransfer(df)			
			else:
				print ('Unknown file type')
							


class buttonWidget(QWidget):
	""" This is the main buton widget """

	# Define signals to be emitted from widget
	statusUpdate = pyqtSignal(str)
	ivSignal = pyqtSignal()
	outputSignal = pyqtSignal()
	transferSignal = pyqtSignal()
	runAllSignal = pyqtSignal()

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

		#runAllBtn = QPushButton('Run All')
		#grid.addWidget(runAllBtn, 2, 2)       
		#runAllBtn.clicked.connect(self.transferSweep)        


	def ivSweep(self, event):
		self.statusUpdate.emit('Performing IV Sweep.')
		self.ivSignal.emit()

	def outputSweep(self, event):
		self.statusUpdate.emit('Performing Output Sweep.')
		self.outputSignal.emit()

	def transferSweep(self, event):
		self.statusUpdate.emit('Performing Transfer Sweep.') 
		self.transferSignal.emit()

	def runAllSweeps(self, event):
		self.statusUpdate.emit('Performing ALL Sweeps.') 
		self.runAllSignal.emit()        


class mplWidget(FigureCanvas):
	""" Widget for matplotlib figure """

	def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
		self.initWidget()

	def initWidget(self, parent = None, width = 5, height = 4, dpi = 100):

		style.use('ggplot')
		#fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2, 2, figsize=(20, 10), dpi= 80, facecolor='w', edgecolor='k')

		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.ax1 = self.fig.add_subplot(111)

		self.ax1.set_title('IV Sweep')
		self.ax1.set_xlabel('Channel Voltage [V]')
		self.ax1.set_ylabel('Channel Current [A]')                

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		
	def drawIV(self, df):
		'''Take a data frame a draw it'''
		self.ax1.plot(df['Channel Voltage [V]'], df['Channel Current [A]'], '.')
		self.ax1.set_title('IV Sweep')
		self.ax1.set_xlabel('Channel Voltage [V]')
		self.ax1.set_ylabel('Channel Current [A]')  		
		FigureCanvas.draw(self)
		
	def drawOutput(self, df):
		'''Take a data frame a draw it'''
		self.ax1.plot(df['Channel Voltage [V]'], df['Channel Current [A]'], '.')
		self.ax1.set_title('Output curves')
		self.ax1.set_xlabel('Channel Voltage [V]')
		self.ax1.set_ylabel('Channel Current [A]')			
		FigureCanvas.draw(self)
		
	def drawTransfer(self, df):
		'''Take a data frame a draw it'''
		self.ax1.plot(df['Gate Voltage [V]'], df['Channel Current [A]'], '.')
		self.ax1.set_title('Transfer Curve')
		self.ax1.set_xlabel('Gate Voltage [V]')
		self.ax1.set_ylabel('Channel Current [A]') 		
		FigureCanvas.draw(self)	
		
	def clear(self):
		'''Clear the plot'''
		self.ax1.clear()
		FigureCanvas.draw(self)

class keithleySettingsWindow(QWidget):
	""" This is the keithley settings widget """

	# Define signals to be emitted from widget
	statusUpdate = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initWidget()

	def initWidget(self):

		# Set widget layout
		grid = QGridLayout()
		self.setLayout(grid)
		# Columns
		col1 = QLabel('Initial Voltage')
		col2 = QLabel('Final Voltage')
		col3 = QLabel('Voltage Step')
		col4 = QLabel('Step Time')
		grid.addWidget(col1, 1, 2)
		grid.addWidget(col2, 1, 3)
		grid.addWidget(col3, 1, 4)
		grid.addWidget(col4, 1, 5)
		# Rows
		row1 = QLabel('IV')
		row2 = QLabel('Ouput')
		row3 = QLabel('Transfer')
		grid.addWidget(row1, 2, 1)
		grid.addWidget(row2, 3, 1)
		grid.addWidget(row3, 4, 1)
		
		
		# IV Settings
		ivFirstV = QDoubleSpinBox(self)
		grid.addWidget(ivFirstV, 2, 2)
		ivLastV = QDoubleSpinBox(self)
		grid.addWidget(ivLastV, 2, 3)
		ivStepV = QDoubleSpinBox(self)
		grid.addWidget(ivStepV, 2, 4)
		ivStepT = QDoubleSpinBox(self)
		grid.addWidget(ivStepT, 2, 5)		
		#ivBtn.clicked.connect(self.ivSweep)
		
		# Ouptut curve Settings
		outputFirstV = QDoubleSpinBox(self)
		grid.addWidget(outputFirstV, 3, 2)
		outputLastV = QDoubleSpinBox(self)
		grid.addWidget(outputLastV, 3, 3)
		outputStepV = QDoubleSpinBox(self)
		grid.addWidget(outputStepV, 3, 4)
		outputStepT = QDoubleSpinBox(self)
		grid.addWidget(outputStepT, 3, 5)		
		#ivBtn.clicked.connect(self.ivSweep)
		
		# transfer Settings
		transferFirstV = QDoubleSpinBox(self)
		grid.addWidget(transferFirstV, 4, 2)
		transferLastV = QDoubleSpinBox(self)
		grid.addWidget(transferLastV, 4, 3)
		transferStepV = QDoubleSpinBox(self)
		grid.addWidget(transferStepV, 4, 4)
		transferStepT = QDoubleSpinBox(self)
		grid.addWidget(transferStepT, 4, 5)		
		#ivBtn.clicked.connect(self.ivSweep)		

		# Window setup
		#self.resize(400, 300)
		self.centre()
		self.setWindowTitle('K2636 - Settings')
		self.show()        

	def centre(self):
		'''Find screen size and place in centre'''

		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width()-size.width())/2, 
	          (screen.height()-size.height())/2)        


class keithleyConnectionWindow(QWidget):
	""" This is the keithley connection widget """

	# Define signals to be emitted from widget
	statusUpdate = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initWidget()

	def initWidget(self):

		# Set widget layout
		grid = QGridLayout()
		self.setLayout(grid)
	
		# Connection status box
		self.connStatus = QTextEdit('Push button to connect to keithley...')
		self.connButton = QPushButton('Connect')
		self.connButton.clicked.connect(self.connect2keithley)
		grid.addWidget(self.connStatus, 1, 1)
		grid.addWidget(self.connButton, 2, 1)
		
		# Window setup
		self.resize(300, 100)
		self.centre()
		self.setWindowTitle('K2636 - Connecting')
		self.show()        

	def centre(self):
		'''Find screen size and place in centre'''

		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width()-size.width())/2, 
		          (screen.height()-size.height())/2)
		
	def connect2keithley(self):
		try:
			self.keithley = k2636.keithley(address='ASRL/dev/ttyUSB0', read_term='\n', baudrate=57600)
			self.connStatus.append('Connection successful')
		except:
			self.connStatus.append('No connection')
			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = ofet_GUI()
	sys.exit(app.exec_())