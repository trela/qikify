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

from ConfigParser import ConfigParser
from glob import glob
import csv

from helpers.general import *
from helpers.plots import *
from models.Specs import *
from models.DatasetTI import *
from controllers.kde import KDE
from controllers.lsfs import LSFS
from controllers.svm import SVM


# All this does is go through every data file and identify fail counts per performance.
# Then, we can easily sum these up to get total fail counts per performance across all devices.
if __name__ == "__main__":
	
	# Controller class instances
	config 	  	= ConfigParser(); config.read('settings.conf')
	specs     	= Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
	lsfs 	  	= LSFS.LSFS()
	kde       	= KDE.KDE()
	svm 		= SVM.SVM()		

	# Read in first wafer, subset by removing discrete ORBiT tests / performances.
	dataFiles = glob(config.get('Settings', 'dataFiles'))
	baseData  = DatasetTI(dataFiles[0])
	baseData.printSummary()
	ind 	  = baseData.genSubsetIndices(specs)
	
	# Iterate over remaining data files and count up fails
	totalDevices = baseData.nrow
	failCounts = []
	failCounts.append(sum(baseData['sData'].pfMat == -1,0).tolist())
	for i, dataFile in enumerate(dataFiles[1:len(dataFiles)]):
		dataset	= DatasetTI(dataFile).clean(specs, ind)
		failCounts.append(sum(dataset['sData'].pfMat == -1,0).tolist())
		totalDevices += dataset.nrow
		print i, totalDevices
	
	# Save counts to a CSV file.
	outData = [baseData['sData'].names.tolist(), sum(array(failCounts),0).tolist()]
	csvWriteMatrix(config.get('Settings', 'resultDir') + 'Specification Test Fail Counts.csv', outData)
