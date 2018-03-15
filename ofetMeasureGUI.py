"""
Qt5 GUI for making OFET measurements with a Keithley 2636.

Author:  Ross <peregrine dot warren at physics dot ox dot ac dot uk>
"""

import k2636  # Driver for keithley 2636
import sys
import fnmatch
import pandas as pd
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QMainWindow, QDockWidget, QWidget, QDesktopWidget,
                             QApplication, QGridLayout, QPushButton, QLabel,
                             QDoubleSpinBox, QAction, qApp, QSizePolicy,
                             QTextEdit, QFileDialog, QInputDialog, QLineEdit)

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as mplToolb
import matplotlib.style as style
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")


class mainWindow(QMainWindow):
    """Create mainwindow of GUI."""

    def __init__(self):
        """Initalise mainwindow."""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Make signal connections."""
        # Add central widget
        self.mainWidget = mplWidget()
        self.setCentralWidget(self.mainWidget)

        # Add other window widgets
        self.keithleySettingsWindow = keithleySettingsWindow()
        self.keithleyConnectionWindow = keithleyConnectionWindow()
        self.popupWarning = warningWindow()

        # Dock setup
        # Keithley dock widget
        self.buttonWidget = keithleyButtonWidget()
        self.dockWidget1 = QDockWidget('Keithley Control')
        self.dockWidget1.setWidget(self.buttonWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget1)

        # Matplotlib control widget
        self.dockWidget2 = QDockWidget('Plotting controls')
        self.dockWidget2.setWidget(mplToolb(self.mainWidget, self))
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget2)

        # Menu bar setup
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
        keithleyConAction.setShortcut('Ctrl+J')
        keithleyConAction.setStatusTip('Reconnect to keithley 2636')
        keithleyAction.triggered.connect(self.keithleySettingsWindow.show)
        keithleyConAction.triggered.connect(self.keithleyConnectionWindow.show)

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

        # Attempt to connect to a keithley
        self.testKeithleyConnection()
        self.keithleyConnectionWindow.connectionSig.connect
        (self.buttonWidget.showButtons)

        # Window setup
        self.resize(800, 800)
        self.centre()
        self.setWindowTitle('K2636 - OFET Measurements')
        self.show()

    def testKeithleyConnection(self):
        """Connect to the keithley on initialisation."""
        try:
                self.keithley = k2636.K2636(address='ASRL/dev/ttyUSB0',
                                            read_term='\n', baudrate=57600)
                self.statusbar.showMessage('Keithley found.')
                self.buttonWidget.showButtons()
                self.keithley.closeConnection()
        except ConnectionError:
                self.buttonWidget.hideButtons()
                self.statusbar.showMessage('No keithley connection.')

    def centre(self):
            """Find screen size and place in centre."""
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width()-size.width())/2,
                      (screen.height()-size.height())/2)

    def showFileOpen(self):
            """Pop up for file selection."""
            filt1 = '*.csv'
            fname = QFileDialog.getOpenFileName(self, 'Open file', filter=filt1)
            if fname[0]:
                    try:
                            df = pd.read_csv(fname[0], '\t')
                            if fnmatch.fnmatch(fname[0], '*iv-sweep.csv'):
                                    self.mainWidget.drawIV(df)
                            elif fnmatch.fnmatch(fname[0], '*output.csv'):
                                    self.mainWidget.drawOutput(df)
                            elif fnmatch.fnmatch(fname[0], '*transfer.csv'):
                                    self.mainWidget.drawTransfer(df)
                            elif fnmatch.fnmatch(fname[0], '*gate-leakage.csv'):
                                    self.mainWidget.drawLeakage(df)
                            else:
                                raise FileNotFoundError
                    except KeyError or FileNotFoundError:
                            self.popupWarning.showWindow('Unsupported file.')

    def updateStatusbar(self, s):
        """Put text in status bar."""
        self.statusbar.showMessage(s)


class keithleyButtonWidget(QWidget):
        """Defines class with buttons controlling keithley."""

        # Define signals to be emitted from widget
        cancelSignal = pyqtSignal()

        def __init__(self):
            """Initialise setup of widget."""
            super().__init__()
            self.initWidget()

        def initWidget(self):
            """Initialise connections."""
            # Set widget layout
            grid = QGridLayout()
            self.setLayout(grid)

            # Push button setup
            self.ivBtn = QPushButton('IV Sweep')
            grid.addWidget(self.ivBtn, 1, 1)
            self.ivBtn.clicked.connect(self.showSampleNameInput)

            self.outputBtn = QPushButton('Output Sweep')
            grid.addWidget(self.outputBtn, 1, 2)
            self.outputBtn.clicked.connect(self.showSampleNameInput)

            self.transferBtn = QPushButton('Transfer Sweep')
            grid.addWidget(self.transferBtn, 1, 3)
            self.transferBtn.clicked.connect(self.showSampleNameInput)

            self.allBtn = QPushButton('ALL')
            grid.addWidget(self.allBtn, 1, 4)
            self.allBtn.clicked.connect(self.showSampleNameInput)

            self.inverterBtn = QPushButton('Voltage Inverter')
            grid.addWidget(self.inverterBtn, 2, 1)
            self.inverterBtn.clicked.connect(self.showSampleNameInput)

        def showSampleNameInput(self):
            """Popup for sample name input."""
            samNam = QInputDialog()
            try:
                text, ok = samNam.getText(self, 'Sample Name',
                                          'Enter sample name:',
                                          QLineEdit.Normal,
                                          str(self.SampleName))

            except AttributeError:
                text, ok = samNam.getText(self, 'Sample Name',
                                          'Enter sample name:')
            if ok:
                if text != '':  # to catch empty input
                    self.SampleName = str(text)
            else:
                self.SampleName = None
                self.cancelSignal.emit()  # doesnt link to anything yet

        def hideButtons(self):
            """Hide control buttons."""
            self.ivBtn.setEnabled(False)
            self.outputBtn.setEnabled(False)
            self.transferBtn.setEnabled(False)
            self.allBtn.setEnabled(False)

        def showButtons(self):
            """Show control buttons."""
            self.ivBtn.setEnabled(True)
            self.outputBtn.setEnabled(True)
            self.transferBtn.setEnabled(True)
            self.allBtn.setEnabled(True)


class mplWidget(FigureCanvas):
        """Widget for matplotlib figure."""

        def __init__(self, parent=None):
            """Create plotting widget."""
            self.initWidget()

        def initWidget(self, parent=None, width=5, height=4, dpi=100):
            """Set parameters of plotting widget."""
            style.use('ggplot')  # Looks the best?

            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.ax1 = self.fig.add_subplot(111)

            self.ax1.set_title('IV Sweep')
            self.ax1.set_xlabel('Channel Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')

            FigureCanvas.__init__(self, self.fig)
            self.setParent(parent)
            FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)

        def drawIV(self, df):
            """Take a data frame and draw it."""
            self.ax1 = self.fig.add_subplot(111)
            self.ax1.plot(df['Channel Voltage [V]'], df['Channel Current [A]'],
                          '.')
            self.ax1.set_title('IV Sweep')
            self.ax1.set_xlabel('Channel Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')
            FigureCanvas.draw(self)

        def drawOutput(self, df):
            """Take a data frame and draw it."""
            self.ax1 = self.fig.add_subplot(111)
            self.ax1.plot(df['Channel Voltage [V]'], df['Channel Current [A]'],
                          '.')
            self.ax1.set_title('Output curves')
            self.ax1.set_xlabel('Channel Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')
            FigureCanvas.draw(self)

        def drawTransfer(self, df):
            """Take a data frame and draw it."""
            self.ax1 = self.fig.add_subplot(111)
            self.ax1.semilogy(df['Gate Voltage [V]'],
                              abs(df['Channel Current [A]']), '.')
            self.ax1.set_title('Transfer Curve')
            self.ax1.set_xlabel('Gate Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')
            FigureCanvas.draw(self)

        def drawLeakage(self, df):
            """Take a data frame and draw it."""
            self.ax1 = self.fig.add_subplot(111)
            self.ax1.plot(df['Gate Voltage [V]'], df['Gate Leakage [A]'], '.')
            self.ax1.set_title('Leakage from gate to drain')
            self.ax1.set_xlabel('Gate Voltage [V]')
            self.ax1.set_ylabel('Gate Leakage [A]')
            FigureCanvas.draw(self)

        def drawAll(self, sample):
            """Take all sweeps and draw them."""
            df1 = pd.read_csv(str(sample + '-iv-sweep.csv'), '\t')
            df2 = pd.read_csv(str(sample + '-output.csv'), '\t')
            df3 = pd.read_csv(str(sample + '-transfer.csv'), '\t')

            self.fig.clear()
            self.ax1 = self.fig.add_subplot(221)
            self.ax2 = self.fig.add_subplot(222)
            self.ax3 = self.fig.add_subplot(223)
            self.ax4 = self.fig.add_subplot(224)

            self.ax1.plot(df1['Channel Voltage [V]'],
                          df1['Channel Current [A]'], '.')
            self.ax1.set_title('I-V sweep')
            self.ax1.set_xlabel('Channel Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')

            self.ax2.plot(df2['Channel Voltage [V]'],
                          df2['Channel Current [A]'], '.')
            self.ax2.set_title('Output curves')
            self.ax2.set_xlabel('Channel Voltage [V]')
            self.ax2.set_ylabel('Channel Current [A]')

            self.ax3.plot(df3['Gate Voltage [V]'],
                          df3['Channel Current [A]'], '.')
            self.ax3.set_title('Transfer Curves')
            self.ax3.set_xlabel('Gate Voltage [V]')
            self.ax3.set_ylabel('Channel Current [A]')

            self.ax4.plot(df3['Gate Voltage [V]'], df3['Gate Leakage [A]'], '.')
            self.ax4.set_title('Gate leakage current')
            self.ax4.set_xlabel('Gate Voltage [V]')
            self.ax4.set_ylabel('Gate Leakage [A]')

            self.fig.tight_layout()
            FigureCanvas.draw(self)

        def drawInverter(self, df):
            """Take a data frame and draw it."""
            self.ax1 = self.fig.add_subplot(111)
            self.ax1.plot(df['Channel Voltage [V]'], df['Channel Current [A]'],
                          '.')
            self.ax1.set_title('Inverter')
            self.ax1.set_xlabel('Channel Voltage [V]')
            self.ax1.set_ylabel('Channel Current [A]')
            FigureCanvas.draw(self)

        def clear(self):
            """Clear the plot."""
            self.fig.clear()
            FigureCanvas.draw(self)


class keithleySettingsWindow(QWidget):
        """Keithley settings popup."""

        def __init__(self):
            """Initialise setup."""
            super().__init__()
            self.initWidget()

        def initWidget(self):
            """Initialise connections."""
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

            # Ouptut curve Settings
            outputFirstV = QDoubleSpinBox(self)
            grid.addWidget(outputFirstV, 3, 2)
            outputLastV = QDoubleSpinBox(self)
            grid.addWidget(outputLastV, 3, 3)
            outputStepV = QDoubleSpinBox(self)
            grid.addWidget(outputStepV, 3, 4)
            outputStepT = QDoubleSpinBox(self)
            grid.addWidget(outputStepT, 3, 5)

            # transfer Settings
            transferFirstV = QDoubleSpinBox(self)
            grid.addWidget(transferFirstV, 4, 2)
            transferLastV = QDoubleSpinBox(self)
            grid.addWidget(transferLastV, 4, 3)
            transferStepV = QDoubleSpinBox(self)
            grid.addWidget(transferStepV, 4, 4)
            transferStepT = QDoubleSpinBox(self)
            grid.addWidget(transferStepT, 4, 5)

            # Window setup
            self.centre()
            self.setWindowTitle('K2636 - Settings')

        def centre(self):
            """Find screen size and place in centre."""
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width()-size.width())/2,
                      (screen.height()-size.height())/2)


class keithleyConnectionWindow(QWidget):
        """Popup for connecting to instrument."""

        connectionSig = pyqtSignal()

        def __init__(self):
            """Initialise setup."""
            super().__init__()
            self.initWidget()

        def initWidget(self):
            """Initialise connections."""
            # Set widget layout
            grid = QGridLayout()
            self.setLayout(grid)

            # Connection status box
            self.connStatus = QTextEdit('Push button to connect to keithley...')
            self.connButton = QPushButton('Connect')
            self.connButton.clicked.connect(self.reconnect2keithley)
            grid.addWidget(self.connStatus, 1, 1)
            grid.addWidget(self.connButton, 2, 1)

            # Window setup
            self.resize(300, 100)
            self.centre()
            self.setWindowTitle('K2636 - Connecting')

        def centre(self):
            """Find screen size and place in centre."""
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width()-size.width()) / 2,
                      (screen.height()-size.height()) / 2)

        def reconnect2keithley(self):
            """Reconnect to instrument."""
            try:
                self.keithley = k2636.K2636(address='ASRL/dev/ttyUSB0',
                                            read_term='\n', baudrate=57600)
                self.connStatus.append('Connection successful')
                self.connectionSig.emit()
                self.keithley.closeConnection()

            except ConnectionError:
                self.connStatus.append('No Keithley can be found.')


class warningWindow(QWidget):
        """Warning window popup."""

        def __init__(self):
            """Intial setup."""
            super().__init__()
            self.initWidget()

        def initWidget(self):
            """Initialise connections."""
            # Set widget layout
            grid = QGridLayout()
            self.setLayout(grid)

            # Connection status box
            self.warning = QLabel()
            self.continueButton = QPushButton('Continue')
            self.continueButton.clicked.connect(self.hide)
            grid.addWidget(self.warning, 1, 1)
            grid.addWidget(self.continueButton, 2, 1)

            # Window setup
            self.resize(180, 80)
            self.centre()
            self.setWindowTitle('Error!')

        def centre(self):
            """Find screen size and place in centre."""
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width()-size.width()) / 2,
                      (screen.height()-size.height()) / 2)

        def showWindow(self, s):
            """Write error message and show window."""
            self.warning.setText(s)
            self.show()


if __name__ == '__main__':

        app = QApplication(sys.argv)
        GUI = mainWindow()
        sys.exit(app.exec_())
