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


# Run LSFS for a series of threshold values to determine best threshold.
if __name__ == "__main__":

	# Controller class instances
	config 	  	= ConfigParser(); config.read('settings.conf')
	specs     	= Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
	lsfs 	  	= LSFS.LSFS()
	kde       	= KDE.KDE()
	svm 		= SVM.SVM()

	dataFiles 	 = glob(config.get('Settings', 'dataFiles'))
	baseData  	 = DatasetTI(dataFiles[0])
	baseData.printSummary()
	ind 	  	 = baseData.genSubsetIndices(specs)
	
	nCrossVals   = 10
	thresholds   = [0.15, 0.2, 0.25]
	
	# Iterate over the threshold values
	results = []
	for i, threshold in enumerate(thresholds):
		oDataSubset = baseData['oData'].subsetCols(lsfs.subset(threshold))
		for j in xrange(nCrossVals):
			# Generate training set using KDE
			counts = dotdict({'nGood': N_GOOD, 'nCritical': N_CRITICAL, 'nFail': N_FAIL})
			kdeData   		= baseData['oDataSub'].join(baseData['sDataSub'])	
			synthetic 		= kde.run(kdeData, specs, counts = counts)
			self.synData   	= DatasetTI(oNames = oDataSubset.names, 
								  		sNames = baseData['sDataSub'].names,
								  		oData = synthetic[:,0:lsfs.nRetained], 
								  		sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')
			
			results.append([threshold] + iccad.runSVM())

	csvWriteMatrix(config.get('Settings', 'resultDir') + 'LSFSThresholdErrors.csv', self.results)		
	plotLSFSThresholds(thresholds, results, config.get('Settings', 'resultDir') + 'lsfsThresholds.pdf')





