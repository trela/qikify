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

import csv
from ConfigParser import ConfigParser
from glob import glob
from random import sample

from helpers.general import *
from helpers.plots import *
from models.Specs import *
from models.DatasetTI import *
from controllers.kde import KDE
from controllers.lsfs import LSFS
from controllers.svm import SVM

# Global parameters controlling the run
K_INNER     = 5.5/6        # For KDE, defines critical region
K_OUTER     = 6.5/6        # For KDE, defines critical region
KDE_COUNTS  = dotdict({'nGood': 15000, 'nCritical': 5000, 'nFail': 5000})
T_L         = 0.01
IND_S       = 32           # 'XTR_SN_IDS_X01'
#TRAIN_WAFER = 1

# Controller class instances
config = ConfigParser(); config.read('settings.conf')
specs  = Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
lsfs   = LSFS.LSFS()
kde    = KDE.KDE()
svm    = SVM.SVM()

# Just spit out some information with each run
def printRunInfo(dataFile, errorReal, errorSyn):
    print dataFile[39:50],
    print 'TE:', str(round(errorReal[0],3)) + '%', 'YL:', str(round(errorReal[1],3)) + '%',
    print 'TE:', str(round(errorSyn[0], 3)) + '%', 'YL:', str(round(errorSyn[1], 3)) + '%'


if __name__ == "__main__":
    dataFiles = glob(config.get('Settings', 'dataFiles'))
    baseData  = DatasetTI(dataFiles[0]); baseData.printSummary()
    ind       = baseData.genSubsetIndices(specs)
    specName  = baseData['sData'].names[IND_S]; print 'Analyzing specification', specName
    
    # Run LSFS against the ORBiT data + the retained specification test
    lsfs.run(baseData['oData'].data, baseData['sData'].pfMat[:,IND_S]); lsfs.subset(T_L)
    del baseData
    
    # Construct training dataset for synthetic dataset training
    # use a random sample of 3 wafers
    trainWaferInd = sample(xrange(len(dataFiles)),3)
    print 'KDE: Training on wafers ', ', '.join(map(str, trainWaferInd))
    trainData = DatasetTI(dataFiles[trainWaferInd[0]]).clean(specs, ind)
    for i in xrange(1,len(trainWaferInd)):
        trainData = trainData.joinRows(DatasetTI(dataFiles[trainWaferInd[i]]).clean(specs, ind))
    trainData.computePF(specs, dataset='sData').printSummary()
    
    # Construct synthetic dataset
    kdeData   = trainData['oData'].subsetCols(lsfs.Subset).join(trainData['sData'].subsetCols(IND_S))
    synthetic = kde.run(kdeData, specs, counts=KDE_COUNTS)   
    synData   = DatasetTI(synData=synthetic, nRetained=lsfs.nRetained).computePF(specs, dataset='sData')
    
    # Clean up because always run out of memory here
    del trainData; del synthetic; del kde; kde = KDE.KDE()
  
    # Train SVM
    svm.train(synData['oData'].data, synData['sData'].gnd, gridSearch = True)
    
    # Go through everything else and get TE/YL
    errorReal, errorSyn, runIndex = [], [], 0
    for j, dataFile in enumerate(dataFiles[2:len(dataFiles)]):
        if j in trainWaferInd:
            continue
        
        # Evaluate real data error metrics
        nData      = DatasetTI(dataFile).clean(specs, ind)
        predReal   = svm.predict(nData['oData'].subsetCols(lsfs.Subset).data)
        TE_YL_Real = svm.getTEYL(nData['sData'].pfMat[:,IND_S], predReal)
        errorReal.append(TE_YL_Real)
        
        # Evaluate synthetic data error metrics
        sData     = DatasetTI(synData=kde.run(kdeData, nSamples=int(nData.nrow)), nRetained=lsfs.nRetained).computePF(specs, dataset='sData')
        predSyn   = svm.predict(sData['oData'].data)
        TE_YL_Syn = svm.getTEYL(sData['sData'].pfMat[:,0], predSyn)
        errorSyn.append(TE_YL_Syn)
        
        printRunInfo(dataFile, errorReal[runIndex], errorSyn[runIndex])
        runIndex += 1
        
    plotTEYL(array(errorReal), array(errorSyn), config.get('Settings', 'resultDir') + 'Result  - ' + specName + ' TrainWafer - Random - T_L - ' + str(T_L) + '.pdf')


