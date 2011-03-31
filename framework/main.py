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

import csv, os, glob, numpy, sys, ConfigParser
from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from scikits.learn.metrics import confusion_matrix
from scikits.learn.svm import SVC

from models.Specs import *
from models.DatasetTI import *
from helpers.general import *
from helpers.plots import *
from controllers.kde import KDE
from controllers.lsfs import LSFS


# We first consider the spec which fails most frequently
def findMostFailingSpecPerf(baseData):
	passingRates = (1.0 * sum(baseData.datasets.sData.pfMat == 1,0)) / size(baseData.datasets.sData.pfMat,0) 
	gnd = baseData.datasets.sData.pfMat[:,argmin(passingRates)]
	print 'Retained only specification test ' + helpers.bcolors.FAIL + '#' + str(argmin(passingRates)) + helpers.bcolors.ENDC
	print 'Pass: ' + helpers.bcolors.OKGREEN + str(sum(gnd == 1)) + helpers.bcolors.ENDC, 
	print ' Fail: ' + helpers.bcolors.FAIL + str(sum(gnd == -1)) + helpers.bcolors.ENDC
	return argmin(passingRates)


def runKDE(baseData):
	pass
	'''
	kdeSpecs = Specs()
	
	kde  	 	   = KDE.KDE()
	S	     	   = kde.run(bbb, 
							 a = 0, 
							 specs = specs, 
							 nGood = 10,
							 nCritical = 10,
							 nFail = 100,
							 inner = vstack([ specs.inner[name] for name in baseData.sNames ]),
							 outer = vstack([ specs.outer[name] for name in baseData.sNames ]))
	
	# Create native data structure from KDE results
	synData = DatasetTI(oNames = baseData.oNames, 
						 sNames = baseData.sNames, 
						 oData  = S[:,0:size(baseData.oData,1)],
						 sData  = S[:,  size(baseData.oData,1):])
	synData.computePF(specs)
	plotSample(synData.sData, baseData.sData, 4,5)
	'''

if __name__ == "__main__":
	## ============= Init, load specs ============= ##
	config = ConfigParser.RawConfigParser()
	config.read('settings.conf')
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs(config.get('Settings', 'specFile'))
	specs.genCriticalRegion()
	
	# Load the first wafer and subset rows/cols.
	baseData  = DatasetTI(filename = dataFiles[0])
	baseData.printSummary()
	ind = baseData.genSubsetIndices(specs)
	baseData.printSummary()

	## ============= Run LSFS ============= ##
	specIndex = findMostFailingSpecPerf(baseData)
	lsfs = LSFS.LSFS()
	lsfs.run(baseData.datasets.oData, baseData.datasets.sData.pfMat[:,specIndex])
	lsfs.plotScores(config.get('Settings', 'lsfsPlot'))
	
	
	## ============= Run KDE ============= ##
	runKDE(baseData)







