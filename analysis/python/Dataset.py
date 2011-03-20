from numpy import *

import csv

class Dataset: 
	def __init__(self, filename, hasHeader = True):
		# Read dataset column names
		if ( hasHeader ):
			fileh 	  	= open(filename, 'rU')
			specReader 	= csv.reader(fileh)
			self.names  =  specReader.next()
			fileh.close()
		
		# Read dataset data
		self.data  = loadtxt(filename, delimiter=',', skiprows=1)

		
	def __getitem__(self, name):
		return self.data[:,self.names.index(name)]

	# ===============================================================
	def printSummary(self):
		print '====================================='
		print ' Dataset\t# Rows\t# Cols'
		print '====================================='
		print 'All data\t' + str(size(self.data,0)) + '\t' + str(size(self.data,1))
		
		if hasattr(self, 'gnd'):
			print '====================================='
			print 'Pass\t' + str(sum(self.gnd == 1))
			print 'Fail\t' + str(sum(self.gnd == -1))
