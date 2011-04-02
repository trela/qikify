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

from helpers.general import *
from helpers.plots import *
from models.Specs import *
from models.DatasetTI import *
from controllers.kde import KDE
from controllers.lsfs import LSFS
from controllers.svm import SVM


# Global parameters controlling the run
THRESH_LSFS = 0.02		# Threshold determining how many features are retained by LSFS
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

# Results go here
error    = zeros((len(dataFiles[1:len(dataFiles)]), 2))
errorSyn = zeros((len(dataFiles[1:len(dataFiles)]), 2))


def runAll(dataFiles, baseData, kdeData):
	for i, dataFile in enumerate(dataFiles[1:len(dataFiles)]):
		# Evaluate real data error metrics
		dataset 	= DatasetTI(dataFile).clean(specs, ind)
		predicted  	= svm.predict(dataset['oData'].subsetCols(lsfs.Subset).data)
		error[i,:] 	= svm.getTEYL(dataset['sData'].pfMat[:,ind_s], predicted)
		
		# Evaluate synthetic data error metrics	
		synthetic = kde.run(kdeData, nSamples = int(dataset.nrow))
		synData   = DatasetTI(oNames = baseData['oData'].names, 
							  sNames = baseData['sData'].names,
							  oData = synthetic[:,0:lsfs.nRetained], 
							  sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')
		errorSyn[i,:] = svm.getTEYL(synData['sData'].gnd, svm.predict(synData['oData'].data))
	
		print dataFile[39:50], 
		print 'TE:', str(round(error[i,0], 3)) + '%', 
		print 'YL:', str(round(error[i,1], 3)) + '%',
		print 'TE:', str(round(errorSyn[i,0], 3)) + '%',
		print 'YL:', str(round(errorSyn[i,1], 3)) + '%'
	
	plotTEYL(error, errorSyn, '/Users/nathankupp/Desktop/Result ' + str(THRESH_LSFS) + ' - ' + str(N_GOOD) + ' - ' + str(N_CRITICAL) + ' - ' + str(N_FAIL) + '.png')
	
	
	
if __name__ == "__main__":
	dataFiles = glob(config.get('Settings', 'dataFiles'))
	baseData  = DatasetTI(dataFiles[0])
	baseData.printSummary()
	ind 	  = baseData.genSubsetIndices(specs)
	
	# Identify the most-frequently failing specification test.
	# Run LSFS against the ORBiT data + the retained specification test.
	ind_s     = argmin( sum(baseData['sData'].pfMat == 1,0) / baseData['sData'].nrow)
	gnd  	  = baseData['sData'].pfMat[:,ind_s]
	lsfs.run(baseData['oData'], gnd, plot = config.get('Settings', 'lsfsPlot'))
	lsfs.subset(THRESH_LSFS)
	baseData.subsetCols({'oData': lsfs.Subset, 'sData': ind_s})
	
	# KDE
	kdeData   = baseData['oData'].join(baseData['sData'])	
	synthetic = kde.run(kdeData, specs, counts = dotdict({'nGood': N_GOOD, 'nCritical': N_CRITICAL, 'nFail': N_FAIL}))
	synData   = DatasetTI(oNames = baseData['oData'].names, 
						  sNames = baseData['sData'].names,
						  oData = synthetic[:,0:lsfs.nRetained], 
						  sData = array([synthetic[:,-1]]).T).computePF(specs, dataset = 'sData')

	# SVM
	svm.train(synData['oData'].data, synData['sData'].gnd, gridSearch = True)
	svm.getTEYL(gnd, svm.predict(baseData['oData'].data))

	# Go through everything else and get TE/YL
	runAll(dataFiles, baseData, kdeData)
	




