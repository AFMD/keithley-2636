#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OFET measurement main program linking gui and measurement thread.

Author:  Ross <peregrine dot warren at physics dot ox dot ac dot uk>
"""

import ofetMeasureGUI  # GUI
import k2636  # driver
import sys
import time
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication


class GUI(ofetMeasureGUI.mainWindow):
    """GUI linked to measurement thread."""

    def __init__(self):
        """Take GUI and add measurement thread connection."""
        super().__init__()
        self.params = {}  # for storing parameters
        self.setupConnections()

    def setupConnections(self):
        """Connect the GUI to the measurement thread."""
        self.buttonWidget.ivBtn.clicked.connect(self.ivSweep)
        self.buttonWidget.outputBtn.clicked.connect(self.outputSweep)
        self.buttonWidget.transferBtn.clicked.connect(self.transferSweep)
        self.buttonWidget.allBtn.clicked.connect(self.allMeasurements)
        self.buttonWidget.inverterBtn.clicked.connect(self.inverter)

    def ivSweep(self):
        """Perform IV sweep."""
        try:
            if self.buttonWidget.SampleName is None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing IV Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'iv-sweep'
            self.measureThread = measureThread(self.params)
            self.measureThread.finishedSig.connect(self.done)
            self.measureThread.start()
        except AttributeError or KeyError:
            self.popupWarning.showWindow('No sample name given!')

    def outputSweep(self, event):
        """Perform output sweep."""
        try:
            if self.buttonWidget.SampleName is None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing Output Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'output'
            self.measureThread = measureThread(self.params)
            self.measureThread.finishedSig.connect(self.done)
            self.measureThread.start()
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')

    def transferSweep(self, event):
        """Perform transfer sweep."""
        try:
            if self.buttonWidget.SampleName is None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing Transfer Sweep...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'transfer'
            self.measureThread = measureThread(self.params)
            self.measureThread.finishedSig.connect(self.done)
            self.measureThread.errorSig.connect(self.error)
            self.measureThread.start()
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')

    def allMeasurements(self, event):
        """Perform all sweeps."""
        try:
            if self.buttonWidget.SampleName is None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing all...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'all'
            self.measureThread = measureThread(self.params)
            self.measureThread.finishedSig.connect(self.done)
            self.measureThread.errorSig.connect(self.error)
            self.measureThread.start()
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')

    def inverter(self, event):
        """Perform voltage inverter measurement."""
        try:
            if self.buttonWidget.SampleName is None:
                raise AttributeError
            self.params['Sample name'] = self.buttonWidget.SampleName
            self.statusbar.showMessage('Performing inverter measurement...')
            self.buttonWidget.hideButtons()
            self.params['Measurement'] = 'inverter'
            self.measureThread = measureThread(self.params)
            self.measureThread.finishedSig.connect(self.done)
            self.measureThread.errorSig.connect(self.error)
            self.measureThread.start()
        except AttributeError:
            self.popupWarning.showWindow('No sample name given!')

    def done(self):
        """Update display when finished measurement."""
        self.statusbar.showMessage('Measurement(s) complete.')
        self.dislpayMeasurement()
        self.buttonWidget.showButtons()

    def error(self, message):
        """Raise error warning."""
        self.popupWarning.showWindow(str(message))
        self.statusbar.showMessage('Measurement error!')
        self.buttonWidget.hideButtons()

    def dislpayMeasurement(self):
        """Display the data on screen."""
        try:
            # IV sweep display
            if self.params['Measurement'] == 'iv-sweep':
                df = pd.read_csv(str(self.params['Sample name'] + '-' +
                                 self.params['Measurement'] + '.csv'), '\t')
                self.mainWidget.drawIV(df)
            # OUTPUT sweep display
            elif self.params['Measurement'] == 'output':
                df = pd.read_csv(str(self.params['Sample name'] + '-' +
                                 self.params['Measurement'] + '.csv'), '\t')
                self.mainWidget.drawOutput(df)
            # TRANSFER sweep display
            elif self.params['Measurement'] == 'transfer':
                df = pd.read_csv(str(self.params['Sample name'] + '-neg-pos-' +
                                 self.params['Measurement'] + '.csv'), '\t')
                self.mainWidget.drawTransfer(df)
            # ALL sweeps display
            elif self.params['Measurement'] == 'all':
                self.mainWidget.drawAll(str(self.params['Sample name']))
            # INVERTER sweep display
            elif self.params['Measurement'] == 'inverter':
                df = pd.read_csv(str(self.params['Sample name'] + '-' +
                                 self.params['Measurement'] + '.csv'), '\t')
                self.mainWidget.drawInverter(df)

        except FileNotFoundError:
            self.popupWarning.showWindow('Could not find data!')


class measureThread(QThread):
    """Thread for running measurements."""

    finishedSig = pyqtSignal()
    errorSig = pyqtSignal(str)

    def __init__(self, params):
        """Initialise threads."""
        QThread.__init__(self)
        self.params = params

    def __del__(self):
        """When thread is deconstructed wait for porcesses to complete."""
        self.wait()

    def run(self):
        """Logic to be run in background thread."""
        try:
            keithley = k2636.K2636()
            begin_measure = time.time()

            if self.params['Measurement'] == 'iv-sweep':
                keithley.IVsweep(self.params['Sample name'])

            if self.params['Measurement'] == 'output':
                keithley.Output(self.params['Sample name'])

            if self.params['Measurement'] == 'transfer':
                keithley.Transfer(self.params['Sample name'])

            if self.params['Measurement'] == 'all':
                keithley.IVsweep(self.params['Sample name'])
                keithley.Output(self.params['Sample name'])
                keithley.Transfer(self.params['Sample name'])

            if self.params['Measurement'] == 'inverter':
                keithley.Inverter(self.params['Sample name'])

            keithley.closeConnection()
            self.finishedSig.emit()
            finish_measure = time.time()
            print('-------------------------------------------\nAll measurements complete. Total time % .2f mins.'
                  % ((finish_measure - begin_measure) / 60))

        except ConnectionError:
            self.errorSig.emit('No measurement made. Please retry.')
            self.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainGUI = GUI()
    sys.exit(app.exec_())
