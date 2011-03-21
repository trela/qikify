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

from Dataset import * 

class Dataset_TI(Dataset):
	
	def __init__(self, filename = None):
		if filename is not None:
			# Read dataset column names
			fileh 	  	= open(filename, 'rU')
			specReader 	= csv.reader(fileh)
			self.names  =  array(specReader.next())
			fileh.close()
		
			# Read dataset
			self.data   = loadtxt(filename, delimiter=',', skiprows=1)
			self.sData  = self.data[:,739:];
			self.sNames = self.names[ 739:];
			self.oData  = self.data[:,0:739];
			self.oNames = self.names[ 0:739];
		

	# Run on first dataset, baseData, to:
	# 1. Create logical column index vector which retains only features with more than 100 unique values.
	# 2. Compute pass/fail for all devices.
	# 3. Identify rows to retain by excluding outliers > 3 sigma from mean.
	# 4. Update retained index list to exclude always-passing specs.
	def initSubsetIndices(self, specs):
		ind = dotdict({'sData': apply_along_axis(lambda x: len(unique(x)) > 100, 0, self.sData),
					   'oData': apply_along_axis(lambda x: len(unique(x)) > 100, 0, self.oData)})
		
		self.computePF(specs, ind);
		
		indRows    = self.idOutliers(True, ind)
		ind.sData  = logical_and(ind.sData, (sum(self.pfMat[indRows,:],0) / sum(indRows) != 1))
		
		self.subsetCols(ind)
		self.subsetRows(indRows)
		self.computePF(specs)
		return ind
		
	# Identify outliers. If "all" parameter is set, do so on the basis of *both* spec & ORBiT
	# measurements. Otherwise, only use ORBiT measurements to ID outliers.
	def idOutliers(self, all, ind):
		cData = hstack((self.oData[:,ind.oData], self.sData[:,ind.sData])) if all else self.oData	
		return ~any(abs(cData - cData.mean(axis = 0)) > 3 * cData.std(axis = 0),1)


	# Compute pass/fail
 	def computePF(self, specs, ind = None):
		n, p       = size(self.sData,0), size(self.sData,1)
		self.pfMat = ones((n,p))
		for j in range(0,p):
			lsl, usl = specs[self.sNames[j]]
			if type(ind) is dict and ~(ind.sData[j]):
				continue
			else:
				self.pfMat[:,j]  = compareToSpecs(self.sData[:,j], lsl, usl)
		self.gnd = bool2symmetric(sum(self.pfMat, 1) == p)




	# ===============================================================

	def subsetCols(self, ind):
		if 'sData' in ind.keys():
			self.sData  = self.sData[:,ind.sData]
			self.sNames = self.sNames[ ind.sData]
		if 'oData' in ind.keys():	
			self.oData  = self.oData[:,ind.oData]
			self.oNames = self.oNames[ ind.oData]

	def subsetRows(self, indRows):
		self.sData  = self.sData[indRows,:]
		self.oData  = self.oData[indRows,:]
	
	def printSummary(self):
		print '====================================='
		print ' Dataset\t# Rows\t# Cols'
		print '====================================='
		if hasattr(self, 'data'):
			print 'All data\t' + str(size(self.data,0)) + '\t' + str(size(self.data,1))
		print 'ORBiT\t\t' + str(size(self.oData,0)) + '\t' + str(size(self.oData,1))
		print 'Spec Data\t' + str(size(self.sData,0)) + '\t' + str(size(self.sData,1))
		
		if hasattr(self, 'gnd'):
			print '====================================='
			print 'Pass\t' + str(sum(self.gnd == 1))
			print 'Fail\t' + str(sum(self.gnd == -1))
			