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
import csv, sys

from helpers.general import *
from helpers.plots import *
from models.Specs import *
from models.DatasetTI import *
from controllers.kde import KDE
from controllers.lsfs import LSFS
from controllers.svm import SVM

# Global parameters controlling the run
K_INNER		= 5.5/6		# For KDE, defines critical region
K_OUTER 	= 6.5/6		# For KDE, defines critical region
N_GOOD 		= 1000
N_CRITICAL  = 200
N_FAIL		= 200

# Controller class instances
config 	  	= ConfigParser(); config.read('settings.conf')
specs     	= Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
lsfs 	  	= LSFS.LSFS()
kde       	= KDE.KDE()
svm 		= SVM.SVM()

	
# Run LSFS for a series of threshold values to determine best threshold.
if __name__ == "__main__":
	if len(sys.argv) == 2:
		ind_s = int(sys.argv[1])
	else:
		sys.exit()
	
	dataFiles 	 = glob(config.get('Settings', 'dataFiles'))
	baseData  	 = DatasetTI(dataFiles[0])
	baseData.printSummary()
	ind 	  	 = baseData.genSubsetIndices(specs)

	thresholds   = [0.006, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
	nCrossVals	 = 5
	
	
	## Main run given ind_s
	print ind_s, baseData['sData'].names[ind_s]
	printPassFail(baseData['sData'].pfMat[:,ind_s])

	lsfs.run(baseData['oData'].data, baseData['sData'].pfMat[:,ind_s])
	baseData['sDataSub'] = baseData['sData'].subsetCols(ind_s)
	
	# Iterate over the threshold values
	results = []
	for i, threshold in enumerate(thresholds):
		baseData['oDataSub'] = baseData['oData'].subsetCols(lsfs.subset(threshold))
		kdeData   			 = baseData['oDataSub'].join(baseData['sDataSub'])
		
		for j in xrange(nCrossVals):
			# Generate training set using KDE
			synthetic = kde.run(kdeData, specs, counts = dotdict({'nGood': N_GOOD, 'nCritical': N_CRITICAL, 'nFail': N_FAIL}))
			synData   = DatasetTI(oNames = baseData['oDataSub'].names, 
								  sNames = baseData['sDataSub'].names,
								  oData = synthetic[:,0:lsfs.nRetained], 
								  sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')

			svm.train(synData['oData'].data, synData['sData'].gnd, gridSearch = True)
			results.append([threshold] + svm.getTEYL(baseData['sData'].pfMat[:,ind_s], svm.predict(baseData['oDataSub'].data)))
			print str(j+1) + '/' + str(nCrossVals), results[-1]

	resultsArray = array(results)
	csvWriteMatrix(config.get('Settings', 'resultDir') + 'LSFSThresholdErrors - ' + baseData['sData'].names[ind_s] + '.csv', results)		
	plotLSFSThresholds(resultsArray, config.get('Settings', 'resultDir') + 'lsfsThresholds - ' + baseData['sData'].names[ind_s] + '.pdf', thresholds)
	print 'Minimum TE at threshold=' + resultsArray[argmin(resultsArray[:,1]),0]	



loadtxt(config.get('Settings', 'resultDir') + 'LSFSThresholdErrors - FM_SNR2_108_R_N47DBM.csv', delimiter=',', skiprows=0)
