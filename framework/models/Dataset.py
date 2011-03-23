#!/usr/bin/python
'''
Copyright (c) 2011 Nathan Kupp, Yale University.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import sys, os, csv
from numpy import *
from helpers.general import * 

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


	def allData(self):
		return self.data

		
	def printSummary(self):
		print '====================================='
		print ' Dataset\t# Rows\t# Cols'
		print '====================================='
		print 'All data\t' + str(size(self.data,0)) + '\t' + str(size(self.data,1))
		
		if hasattr(self, 'gnd'):
			print '====================================='
			print 'Pass\t' + str(sum(self.gnd == 1))
			print 'Fail\t' + str(sum(self.gnd == -1))
