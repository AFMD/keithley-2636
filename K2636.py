#!/usr/bin/env python3
#coding:utf-8

"""
  Author:  Ross
  Purpose: 'Simple' driver for Keithley 2636
  Created: 07/03/17
"""

import visa
import sys
import pandas as pd
import matplotlib.pyplot as plt

########################################################################
class K2636():
	"""Class for Keithley control"""

	#----------------------------------------------------------------------
	def __init__(self, rm, address, read_term, baudrate):
		"""Constructor - makes connection to instrument on instance"""
		self.make_connection(rm, address, read_term, baudrate)
	
	#----------------------------------------------------------------------
	def make_connection (self, rm, address, read_term, baudrate):
		"""Make initial connection to instrument"""
		
		if 'ttyS' or 'ttyUSB' in str(address) :
			# Connection via SERIAL
			print ('Connecting to Keithley via %s' %address)
			self.inst = rm.open_resource(address)
			self.inst.read_termination = str(read_term)
			self.inst.baud_rate = baudrate
			print (self.inst.query('*IDN?'))
			
		if 'GPIB' in str(address):
			# Connection via GPIB
			print ('Please use serial.')
			sys.exit()
			
	#----------------------------------------------------------------------		
	def write(self, m):
		'''Wrapper for the PyVisa write function'''
		assert type(m) == str
		self.inst.write(m)
		
	#----------------------------------------------------------------------		
	def read(self):
		'''Wrapper for the PyVisa read function'''
		r = self.inst.read()
		return r
		
	#----------------------------------------------------------------------		
	def query(self, s):
		'''Wrapper for the PyVisa query function'''
		r = self.inst.query(s)
		return r
	
	#----------------------------------------------------------------------		
	def loadTSP(self, tsp):
		'''Load an anonymous TSP script into the K2636 nonvolatile memory'''
		self.write('loadscript')
		print ('\n---------LOADING TSP-----------')
		line_count = 1
		for line in open(tsp, mode='r'):
			self.write(line)
			print('[%s]\t-->' %line_count, line, end='')
			line_count += 1
		self.write('endscript')
		print ('\n----------SENT TO K2636-----------\n')
				
	#----------------------------------------------------------------------		
	def runTSP(self):
		'''Run the anonymous TSP script currently loaded in the K2636 memory'''	
		self.write('script.anonymous.run()')
		print('Script has been told to run.')
		
	#----------------------------------------------------------------------		
	def readBuffer(self):
		'''Read specified buffer in keithley memory and return a pandas array'''
		vg = [float(x) for x in self.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.sourcevalues)').split(',')]
		ig = [float(x) for x in self.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)').split(',')]
		vd = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)').split(',')]
		c = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
		
		df = pd.DataFrame({'Gate Voltage [V]': vg, 'Channel Voltage [V]' : vd, 'Channel Current [A]': c, 'Gate Leakage [A]': ig})
		return df

		
		
########################################################################
def uploadTSP():
	'''Connects to keithley, uploads TSP instructions and tells keithley to execute'''
	print ('BEGIN')
	#------------------------------------------------------------
	
	rm = visa.ResourceManager('@py') #use py-visa backend
	keithley = K2636(rm, address='ASRL/dev/ttyUSB0', read_term='\n', baudrate=57600)
	
	#-------------------------------------------------------------
	sample = 'znpc-5wtpc-20um-3'
	
	#-------------------------------------------------------------
	#print ('Uploading TSP script: ')
	#keithley.loadTSP('TSP-scripts/iv-sweep.tsp')
	#keithley.runTSP()
	#df = keithley.readBuffer()
	#output_name = str(sample + '-iv-sweep.csv')
	#df.to_csv(output_name, sep='\t', index=False)	
	
	print ('Uploading TSP script: ')
	keithley.loadTSP('TSP-scripts/output-charact.tsp')
	keithley.runTSP()
	df = keithley.readBuffer()
	output_name = str(sample + '-output.csv')
	df.to_csv(output_name, sep='\t', index=False)
	
	print ('Uploading TSP script: ')
	keithley.loadTSP('TSP-scripts/transfer-charact.tsp')
	keithley.runTSP()
	df = keithley.readBuffer()
	output_name = str(sample + '-transfer.csv')
	df.to_csv(output_name, sep='\t', index=False)
	
	print ('Uploading TSP script: ')
	keithley.loadTSP('TSP-scripts/gate-leakage.tsp')
	keithley.runTSP()
	df = keithley.readBuffer()
	output_name = str(sample + '-gate-leakage.csv')
	df.to_csv(output_name, sep='\t', index=False)		
	
	#------------------------------------------------------------
	
	rm.close()
	
	#------------------------------------------------------------
	
	df1 = pd.read_csv(str(sample+'-iv-sweep.csv'),'\t')
	plt.plot(df1['Channel Voltage [V]'], df1['Channel Current [A]'], '.')
	plt.show()
	df2 = pd.read_csv(str(sample+'-output.csv'),'\t')
	plt.plot(df2['Channel Voltage [V]'], df2['Channel Current [A]'], '.')
	plt.show()
	df3 = pd.read_csv(str(sample+'-transfer.csv'),'\t')
	plt.plot(df3['Gate Voltage [V]'], df3['Channel Current [A]'], '.')
	plt.show()
	df4 = pd.read_csv(str(sample+'-gate-leakage.csv'),'\t')
	plt.plot(df4['Gate Voltage [V]'], df4['Gate Leakage [A]'], '.')
	plt.show()
	
	print ('END')

if __name__ == '__main__':
	uploadTSP()
	
