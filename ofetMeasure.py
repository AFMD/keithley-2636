#!/home/ross/.anaconda3/bin/python
#coding:utf-8

"""
  Author:  Ross <peregrine.warren@physics.ox.ac.uk>
  Purpose: OFET measurement main program linking gui and measurement thread
  Created: 01/06/17
"""

import ofetMeasureGUI # GUI
import k2636 # driver

import sys
import time
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
       
        
########################################################################
class GUI(ofetMeasureGUI.mainWindow):
    """ GUI linked to measurement thread """

    #----------------------------------------------------------------------
    def __init__(self):
        """ Take GUI and add measurement thread connection """
        super().__init__()
        self.params = {} # for storing parameters
        self.setupConnections()
        
        
    #----------------------------------------------------------------------
    def setupConnections(self):
        """ Connecting the GUI to the measurement thread """
        
        self.buttonWidget.ivBtn.clicked.connect(self.ivSweep)
        self.buttonWidget.outputBtn.clicked.connect(self.outputSweep)
        self.buttonWidget.transferBtn.clicked.connect(self.transferSweep)
        self.buttonWidget.allBtn.clicked.connect(self.allMeasurements)
    
    #----------------------------------------------------------------------    
    def ivSweep(self):
        try:
            if self.buttonWidget.SampleName == None:
                raise AttributeError                
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing IV Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'iv-sweep'
            self.measureThread = measureThread(self.params) # create instance of thread
            self.measureThread.finishedSig.connect(self.done) # what to do when thread has finished
            self.measureThread.start() # run thread
        except AttributeError or KeyError:
            self.popupWarning.showWindow('No sample name given!')

    #----------------------------------------------------------------------
    def outputSweep(self, event):
        try:
            if self.buttonWidget.SampleName == None:
                raise AttributeError                        
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing Output Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'output'
            self.measureThread = measureThread(self.params) # create instance of thread
            self.measureThread.finishedSig.connect(self.done) # what to do when thread has finished
            self.measureThread.start() # run thread
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')            

    #----------------------------------------------------------------------
    def transferSweep(self, event):
        try:
            if self.buttonWidget.SampleName == None:
                raise AttributeError            
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing Transfer Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'transfer'
            self.measureThread = measureThread(self.params) # create instance of thread
            self.measureThread.finishedSig.connect(self.done) # what to do when thread has finished
            self.measureThread.errorSig.connect(self.error) # what to do when an error happens
            self.measureThread.start() # run thread
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')             
        
    #----------------------------------------------------------------------
    def allMeasurements(self, event):
        try:
            if self.buttonWidget.SampleName == None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing all...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'all'
            self.measureThread = measureThread(self.params) # create instance of thread
            self.measureThread.finishedSig.connect(self.done) # what to do when thread has finished
            self.measureThread.errorSig.connect(self.error) # what to do when an error happens
            self.measureThread.start() # run thread
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')              

    #----------------------------------------------------------------------
    def done(self):
        self.statusbar.showMessage('Measurement(s) complete.')
        self.dislpayMeasurement()
        self.buttonWidget.showButtons()
        
    #----------------------------------------------------------------------
    def error(self, message):
        self.popupWarning.showWindow(str(message))
        self.statusbar.showMessage('Measurement error!')
        self.buttonWidget.hideButtons() 
    
    
    #----------------------------------------------------------------------
    def dislpayMeasurement(self):
                try:
                    if self.params['Measurement'] == 'iv-sweep':
                        df = pd.read_csv(str(self.params['Sample name'] + '-' + self.params['Measurement'] + '.csv'), '\t')
                        self.mainWidget.drawIV(df)
                    if self.params['Measurement'] == 'output':
                        df = pd.read_csv(str(self.params['Sample name'] + '-' + self.params['Measurement'] + '.csv'), '\t')
                        self.mainWidget.drawOutput(df)	
                    if self.params['Measurement'] == 'transfer':
                        df = pd.read_csv(str(self.params['Sample name'] + '-' + self.params['Measurement'] + '.csv'), '\t')
                        self.mainWidget.drawTransfer(df)
                    elif self.params['Measurement'] == 'all':
                        self.mainWidget.drawAll(str(self.params['Sample name']))                  
                except:
                    self.popupWarning.showWindow('Problem loading data!')
      	



########################################################################
class measureThread(QThread):
    """ Thread for running measurements """
    
    finishedSig = pyqtSignal()
    errorSig = pyqtSignal(str)
    

    #----------------------------------------------------------------------
    def __init__(self, params):
        ''' Constructor '''
        QThread.__init__(self)
        self.params = params
    
    #----------------------------------------------------------------------
    def __del__(self):
        self.wait()
    
    #----------------------------------------------------------------------
    def run(self):
        ''' Logic to be run in background thread '''
        
        try:
            if self.params['Measurement'] == 'iv-sweep':
                try:
                    keithley = k2636.K2636()
                    keithley.IVsweep(self.params['Sample name'])
                    keithley.closeConnection()
                    self.finishedSig.emit()
                except ConnectionError:
                    self.errorSig.emit('Please check keithely connection')
                    self.quit()
            
            if self.params['Measurement'] == 'output':
                try:
                    keithley = k2636.K2636()
                    keithley.Output(self.params['Sample name'])
                    keithley.closeConnection()
                    self.finishedSig.emit()
                except ConnectionError:
                    self.errorSig.emit('Please check keithely connection')                
                    self.quit()
                    
            if self.params['Measurement'] == 'transfer':
                try:
                    keithley = k2636.K2636()
                    keithley.Transfer(self.params['Sample name'])
                    keithley.closeConnection()
                    self.finishedSig.emit()
                except ConnectionError:
                    self.errorSig.emit('Please check keithely connection')
                    self.quit()
                    
            if self.params['Measurement'] == 'all':
                try:
                    keithley = k2636.K2636()
                    keithley.IVsweep(self.params['Sample name'])
                    keithley.Output(self.params['Sample name'])
                    keithley.Transfer(self.params['Sample name'])
                    keithley.closeConnection()
                    self.finishedSig.emit()
                except ConnectionError:
                    self.errorSig.emit('Please check keithely connection')
                    self.quit()
            
        except:
            self.errorSig.emit('No measurement made. Please retry.')
            self.quit()

#----------------------------------------------------------------------
def main(): 
    app = QApplication(sys.argv)
    mainGUI = GUI()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
