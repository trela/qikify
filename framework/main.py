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


THRESH_LSFS = 0.02
KDE_A 		= 0			# For KDE, bandwidth
K_INNER		= 5.0/6		# For KDE, defines critical region
K_OUTER 	= 6.0/6		# For KDE, defines critical region

if __name__ == "__main__":
	## ============= Init, load specs ============= ##
	config 	  = ConfigParser.ConfigParser()
	config.read('settings.conf')
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs(config.get('Settings', 'specFile'))
		
	# Load the first wafer and subset rows/cols.
	baseData  = DatasetTI(filename = dataFiles[0])
	baseData.printSummary()
	ind 	  = baseData.genSubsetIndices(specs)
	baseData.printSummary()

	# Create pair of boundaries defining critical region of specification test space
	specs.genCriticalRegion(baseData.datasets.sData, k_i = K_INNER, k_o = K_OUTER)


	## ============= Run LSFS ============= ##
	passing   = (1.0 * sum(baseData.datasets.sData.pfMat == 1,0)) / size(baseData.datasets.sData.pfMat,0) 
	specIndex = argmin(passing)
	print 'Retained only specification test ' + RED + '#' + str(specIndex + 1) + ENDCOLOR,
	print ' Pass: ' + GREEN + str(sum(baseData.datasets.sData.pfMat[:,specIndex] == 1)) + ENDCOLOR, 
	print ' Fail: ' + RED + str(sum(baseData.datasets.sData.pfMat[:,specIndex] == -1)) + ENDCOLOR
	lsfs 	  = LSFS.LSFS()
	lsfs.run(baseData.datasets.oData, baseData.datasets.sData.pfMat[:,specIndex]).plotScores(config.get('Settings', 'lsfsPlot'))
	baseData.datasets.oDataSubset = baseData.datasets.oData.subsetCols(lsfs.Scores < THRESH_LSFS, 'ORBiT subset using LSFS.')
	print 'Laplacian score feature selection complete. Retained ',
	print GREEN + str(sum(lsfs.Scores < THRESH_LSFS)) + ENDCOLOR + ' ORBiT parameters.'
	
	## ============= Run KDE ============= ##
	kdeData   = baseData.datasets.oDataSubset.join(baseData.datasets.sData.subsetCols(specIndex), 'KDE: ORBiT subset & spec data.')	
	kde       = KDE.KDE()
	synthetic = kde.run(kdeData, specs, a = KDE_A, counts = dotdict({'nGood': 100, 'nCritical': 100, 'nFail': 100}))




