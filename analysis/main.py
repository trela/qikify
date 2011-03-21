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

from modeling.dataset import Dataset, Dataset_TI, Specs
from modeling.helpers.general import *
from modeling.helpers.plots import *
from modeling.kde import KDE


	
if __name__ == "__main__":
	config = ConfigParser.RawConfigParser()
	config.read('settings.conf')
	
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs.Specs(config.get('Settings', 'specFile'))
	
	baseData  = Dataset_TI.Dataset_TI(dataFiles[0])
	baseData.initSubsetIndices(specs)
	baseData.printSummary()
	
	# LSFS will happen here
	baseData.subsetCols(dotdict({'oData': array([82, 96, 42, 100, 108, 107, 68, 118, 92, 9])}))
	baseData.printSummary()

	# Run KDE
	# Create native data structure from KDE results
	kde  	 	   = KDE.KDE(hstack((baseData.oData, baseData.sData)))
	S	     	   = kde.run(2000)	
	synData 	   = Dataset_TI.Dataset_TI()
	synData.oNames = baseData.oNames
	synData.sNames = baseData.sNames
	synData.oData  = S[:,0:size(baseData.oData,1)]
	synData.sData  = S[:,  size(baseData.oData,1):]
	synData.computePF(specs)
	plotSample(synData.sData, baseData.sData, 4,5)




