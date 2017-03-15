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
		print ('----------SENT TO K2636-----------\n')
				
	#----------------------------------------------------------------------		
	def runTSP(self):
		'''Run the anonymous TSP script currently loaded in the K2636 memory'''	
		self.write('script.anonymous.run()')
		print('Script has been told to run.')
		
	#----------------------------------------------------------------------		
	def readBuffer(self):
		'''Read specified buffer in keithley memory and return a pandas dataframe'''
		df = pd.DataFrame()
		df['Gate Voltage [V]'] = [float(x) for x in self.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.sourcevalues)').split(',')]
		df['Channel Voltage [V]'] = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)').split(',')]
		df['Channel Current [A]'] = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
		return df
		
		
########################################################################
def uploadTSP():
	'''Connects to keithley, uploads TSP instructions and tells keithley to execute'''
	print ('BEGIN')
	#------------------------------------------------------------
	
	rm = visa.ResourceManager('@py') #use py-visa backend
	keithley = K2636(rm, address='ASRL/dev/ttyUSB0', read_term='\n', baudrate=57600)
	
	print ('Uploading TSP script: ', sys.argv[1])
	keithley.loadTSP(sys.argv[1])
	keithley.runTSP()
	df = keithley.readBuffer()
	df.to_csv('first_run.csv')	
	rm.close()
	
	#------------------------------------------------------------
	print ('END')

if __name__ == '__main__':
	uploadTSP()
	
