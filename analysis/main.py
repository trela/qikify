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

from modeling.dataset.Specs import *
from modeling.dataset.Dataset_TI import *
from modeling.helpers.general import *
from modeling.helpers.plots import *
from modeling.kde import KDE


	
if __name__ == "__main__":
	## ============= Init & Load Data, Specs ============= ##
	config = ConfigParser.RawConfigParser()
	config.read('settings.conf')
	
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs(config.get('Settings', 'specFile'))
	specs.genCriticalRegion()
	
	baseData  = Dataset_TI(filename = dataFiles[0])
	baseData.printSummary()

	
'''
	## ============= Run KDE ============= ##
	kde  	 	   = KDE.KDE(baseData, a = 0, specs = specs)
	S	     	   = kde.run(nGood = 10, 
							 nCritical = 10, 
							 nFail = 100, 
							 inner = vstack([ specs.inner[name] for name in baseData.sNames ]),
							 outer = vstack([ specs.outer[name] for name in baseData.sNames ]))	
	
	# Create native data structure from KDE results
	synData = Dataset_TI(oNames = baseData.oNames, 
						 sNames = baseData.sNames, 
						 oData  = S[:,0:size(baseData.oData,1)],
						 sData  = S[:,  size(baseData.oData,1):])
	synData.computePF(specs)

	plotSample(synData.sData, baseData.sData, 4,5)
'''

