from numpy import *

import csv

class Dataset: 
	def __init__(self):
		pass
		
	def importData(self, filename):
		# Read dataset column names
		fileh 	  	= open(filename, 'rU')
		specReader 	= csv.reader(fileh)
		self.names  =  specReader.next()
		fileh.close()
		
		# Read dataset data
		self.data  = loadtxt(filename, delimiter=',', skiprows=1)
		return self
		
	def __getitem__(self, name):
		return self.data[:,self.names.index(name)]