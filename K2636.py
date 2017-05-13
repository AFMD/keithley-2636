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
import matplotlib.style as style
import time

########################################################################
class K2636():
	"""Class for Keithley control"""

	#----------------------------------------------------------------------
	def __init__(self, rm, address, read_term, baudrate):
		"""Constructor - makes connection to instrument on instance"""
		#self.make_connection(rm, address, read_term, baudrate)
		pass
	
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
		tsp_dir = 'TSP-scripts/' # Put all tsp scripts in this folder
		
		self.write('loadscript')
		line_count = 1
		for line in open(str(tsp_dir + tsp), mode='r'):
			self.write(line)
			line_count += 1
		self.write('endscript')
		print('----------------------------------------')
		print ('Uploaded TSP script: ', tsp)
				
	#----------------------------------------------------------------------		
	def runTSP(self):
		'''Run the anonymous TSP script currently loaded in the K2636 memory'''	
		self.write('script.anonymous.run()')
		print('Measurement in progress...')
		
	#----------------------------------------------------------------------		
	def readBuffer(self):
		'''Read specified buffer in keithley memory and return a pandas array'''
		vg = [float(x) for x in self.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.sourcevalues)').split(',')]
		ig = [float(x) for x in self.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)').split(',')]
		vd = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)').split(',')]
		c = [float(x) for x in self.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
		
		df = pd.DataFrame({'Gate Voltage [V]': vg, 'Channel Voltage [V]' : vd, 'Channel Current [A]': c, 'Gate Leakage [A]': ig})
		return df
	
	#----------------------------------------------------------------------		
	def displayMeasurements(sample):
		'''Show graphs of measurements'''
		style.use('ggplot')
		fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2, 2, figsize=(20, 10), dpi= 80, facecolor='w', edgecolor='k')
		df1 = pd.read_csv(str(sample+'-iv-sweep.csv'),'\t')
		ax1.plot(df1['Channel Voltage [V]'], df1['Channel Current [A]'], '.')
		ax1.set_title('I-V sweep')
		ax1.set_xlabel('Channel Voltage [V]')
		ax1.set_ylabel('Channel Current [A]')
		
		df2 = pd.read_csv(str(sample+'-output.csv'),'\t')
		ax2.plot(df2['Channel Voltage [V]'], df2['Channel Current [A]'], '.')
		ax2.set_title('Output curves')
		ax2.set_xlabel('Channel Voltage [V]')
		ax2.set_ylabel('Channel Current [A]')	
		
		df3 = pd.read_csv(str(sample+'-transfer.csv'),'\t')
		ax3.plot(df3['Gate Voltage [V]'], df3['Channel Current [A]'], '.')
		ax3.set_title('Transfer Curves')
		ax3.set_xlabel('Gate Voltage [V]')
		ax3.set_ylabel('Channel Current [A]')	
		
		df4 = pd.read_csv(str(sample+'-transfer.csv'),'\t')
		ax4.plot(df4['Gate Voltage [V]'], df4['Gate Leakage [A]'], '.')
		ax4.set_title('Gate leakage current')
		ax4.set_xlabel('Gate Voltage [V]')
		ax4.set_ylabel('Gate Leakage [A]')
		
		fig.tight_layout()
		fig.savefig(sample)
		plt.show()		

	
	#----------------------------------------------------------------------		
	def IVsweep(sample, keithley):
		'''K2636 IV sweep'''
		begin_time = time.time()
		keithley.loadTSP('iv-sweep.tsp')
		keithley.runTSP()
		df = keithley.readBuffer()
		output_name = str(sample + '-iv-sweep.csv')
		df.to_csv(output_name, sep='\t', index=False)
		finish_time = time.time()
		print('IV sweep complete. Elapsed time %.2f mins.' %((finish_time - begin_time)/60))
		
	#----------------------------------------------------------------------		
	def Output(sample, keithley):
		'''K2636 Output sweeps'''
		begin_time = time.time()
		keithley.loadTSP('output-charact.tsp')
		keithley.runTSP()
		df = keithley.readBuffer()
		output_name = str(sample + '-output.csv')
		df.to_csv(output_name, sep='\t', index=False)
		finish_time = time.time()
		print('Output sweeps complete. Elapsed time %.2f mins.' %((finish_time - begin_time)/60))
		
		
	#----------------------------------------------------------------------		
	def Transfer(sample, keithley):
		'''K2636 Transfer sweeps'''
		begin_time = time.time()
		keithley.loadTSP('transfer-charact.tsp')
		keithley.runTSP()
		df = keithley.readBuffer()
		output_name = str(sample + '-transfer.csv')
		df.to_csv(output_name, sep='\t', index=False)
		finish_time = time.time()
		print('Transfer curves measured. Elapsed time %.2f mins.' %((finish_time - begin_time)/60))
		
########################################################################
def uploadTSP():
	'''Connects to keithley, uploads TSP instructions and tells keithley to execute'''
	
	rm = visa.ResourceManager('@py') #use py-visa backend
	keithley = K2636(rm, address='ASRL/dev/ttyUSB0', read_term='\n', baudrate=57600)	
	
	#-------------------------------------------------------------
	sample = 'blank-20um-2'
	start = time.time()
	#-------------------------------------------------------------

	K2636.IVsweep(sample, keithley)
	K2636.Output(sample, keithley)
	K2636.Transfer(sample, keithley)
	
	#------------------------------------------------------------
	
	K2636.displayMeasurements(sample)
	rm.close()
	
	#------------------------------------------------------------
	
	finish = time.time()
	print ('Elapsed time %.2f mins' % ((finish - start)/60))
	print ('END')

if __name__ == '__main__':
	uploadTSP()
	
