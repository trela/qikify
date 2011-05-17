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

import csv, time
from ConfigParser import ConfigParser
from glob import glob
from random import sample

from helpers.general import *
from models.Specs import *
from models.DatasetTI import *
from controllers.kde import KDE
from controllers.lsfs import LSFS
from controllers.svm import SVM

from scikits.learn.feature_selection.univariate_selection import f_classif
import numpy as np




## The objective of this code is to compare various feature selection methods.









# Global parameters controlling the run
T_L    = 0.01

# Controller class instances
config = ConfigParser(); config.read('settings.conf')
specs  = Specs(config.get('Settings', 'specFile'))
lsfs   = LSFS.LSFS()
kde    = KDE.KDE()

# Run LSFS against the ORBiT data + the retained specification test
def runLSFS(baseData):
    X   = baseData['oData'].data[:3000,:]
    gnd = baseData['sData'].gnd[:3000]
    lsfsStart = time.time()
    lsfs.run(X, gnd)
    print 'LSFS: Completed in', time.time() - lsfsStart, 'seconds.'
    return lsfs.subset(T_L)

# Randomly search for best features
def runRandomSearch(baseData, maxiter=100):
    svm       = SVM.SVM()
    X_train   = baseData['oData'].data[:2000,:]
    gnd_train = baseData['sData'].gnd[:2000]
    X_test    = baseData['oData'].data[2000:3000,:]
    gnd_test  = baseData['sData'].gnd[2000:3000]
    ncol      = baseData['oData'].ncol
    rsStart   = time.time()
    
    bestError, bestInd = 100, []
    for iteration in xrange(maxiter):
        indRandom = array(np.random.randint(2,size=ncol), dtype=bool)
        svm.train(X_train[:,indRandom], gnd_train, gridSearch=False)
        predicted = svm.predict(X_test[:,indRandom])
        error     = sum(svm.getTEYL(gnd_test, predicted))
        if error < bestError:
            bestError = error
            bestInd   = indRandom
            print 'Completed', iteration, 'random searches, best error so far:', bestError
        if iteration % 10 == 0:
            print 'Completed', iteration, 'random searches.'
        
    print 'Random search: Completed', maxiter, ' random searches in', time.time() - rsStart, 'seconds.'
    return bestInd
        
    
if __name__ == "__main__":
    dataFiles = glob(config.get('Settings', 'dataFiles'))
    baseData  = DatasetTI(dataFiles[0]); baseData.printSummary()
    ind       = baseData.genSubsetIndices(specs)
    
    # Run LSFS against the ORBiT data + the retained specification test
    #ind_lsfs = runLSFS(baseData)
    
    # Random search
    ind_rand = runRandomSearch(baseData, maxiter=10000)
    
    # Run ANOVA F-score
    #FScores = f_classif(X, gnd)

    # Train SVMs
    #svm_lsfs = SVM.SVM()
    #svm_lsfs.train(baseData['oData'].subsetCols(ind_lsfs).data, baseData['sData'].gnd, gridSearch=False)
    svm_rand = SVM.SVM()
    svm_rand.train(baseData['oData'].subsetCols(ind_rand).data, baseData['sData'].gnd, gridSearch=False)

    # Go through everything else and get TE/YL
    print 'Going through remaining', len(dataFiles)-1, 'data files.'
    error_lsfs, error_rand = [], []
    for j, dataFile in enumerate(dataFiles):
        if j==0:
            continue
        nData = DatasetTI(dataFile).clean(specs, ind)
    
        # Evaluate error metrics for LSFS
        #predicted = svm_lsfs.predict(nData['oData'].subsetCols(ind_lsfs).data)
        #errorLSFS = svm_lsfs.getTEYL(nData['sData'].gnd, predicted)
        #error_lsfs.append(errorLSFS)
        
        # Evaluate error metrics for random search
        predicted = svm_rand.predict(nData['oData'].subsetCols(ind_rand).data)
        errorRand = svm_rand.getTEYL(nData['sData'].gnd, predicted)
        error_rand.append(errorRand)
        
        print dataFile[39:50], errorRand

    csvWriteMatrix('errorRand.csv', errorRand)


