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



if __name__ == "__main__":
	dataFiles = glob(config.get('Settings', 'dataFiles'))
	baseData  = DatasetTI(dataFiles[0]); baseData.printSummary()
	ind 	  = baseData.genSubsetIndices(specs)
	
	# Results stored in these two arrays
	error 	  = []	
	errorSyn  = []
	
	for ind_s in range(baseData.ncol):
		# Run LSFS against the ORBiT data + the retained specification test.
		lsfs.run(baseData['oData'].data, baseData['sData'].pfMat[:,ind_s])
		lsfs.plotScores(config.get('Settings', 'resultDir') + 'lsfsScores - ' + baseData['sData'].names[ind_s] + '.pdf')
		baseData['oDataSub'] = baseData['oData'].subsetCols(lsfs.subset(0.06))

		# Construct synthetic dataset & train SVM.
		kdeData   	= baseData['oDataSub'].join(baseData['sData'].subsetCols(ind_s))	
		synthetic 	= kde.run(kdeData, specs, counts = dotdict({'nGood': N_GOOD, 'nCritical': N_CRITICAL, 'nFail': N_FAIL}))
		synData   	= DatasetTI(oNames = baseData['oDataSub'].names, 
							  	sNames = baseData['sData'].names[ind_s],
							  	oData = synthetic[:,0:lsfs.nRetained], 
							  	sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')
		svm.train(synData['oData'].data, synData['sData'].gnd, gridSearch = True)

		# Go through everything else and get TE/YL
		error.append(zeros((len(dataFiles[1:]), 2)))
		errorSyn.append(zeros((len(dataFiles[1:]), 2)))
		for j, dataFile in enumerate(dataFiles[1:len(dataFiles)]):
			
			# Evaluate real data error metrics
			dataset 		  = DatasetTI(dataFile).clean(specs, ind)
			predicted  		  = svm.predict(dataset['oData'].subsetCols(lsfs.Subset).data)
			error[ind_s][j,:] = svm.getTEYL(dataset['sData'].pfMat[:,ind_s], predicted)

			# Evaluate synthetic data error metrics	
			synthetic = kde.run(kdeData, nSamples = int(dataset.nrow))
			synData   = DatasetTI(oNames = baseData['oData'].names, 
								  sNames = baseData['sData'].names,
								  oData = synthetic[:,0:lsfs.nRetained], 
								  sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')
			errorSyn[ind_s][j,:] = svm.getTEYL(synData['sData'].gnd, svm.predict(synData['oData'].data))

			print dataFile[39:50],
			print 'TE:', str(round(error[ind_s][j,0], 3)) + '%', 
			print 'YL:', str(round(error[ind_s][j,1], 3)) + '%',
			print 'TE:', str(round(errorSyn[ind_s][j,0], 3)) + '%',
			print 'YL:', str(round(errorSyn[ind_s][j,1], 3)) + '%'
			
		plotTEYL(error[ind_s], errorSyn[ind_s], config.get('Settings', 'resultDir') + 'Result  - ' + baseData['sData'].names[ind_s] + '.pdf')


	
	
	
