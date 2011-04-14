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

import cProfile

# Global parameters controlling the run
K_INNER        = 5.5/6        # For KDE, defines critical region
K_OUTER     = 6.5/6        # For KDE, defines critical region
N_GOOD         = 1000
N_CRITICAL  = 200
N_FAIL        = 200

# Controller class instances
config           = ConfigParser(); config.read('settings.conf')
specs         = Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
lsfs           = LSFS.LSFS()
kde           = KDE.KDE()
svm         = SVM.SVM()


dataFiles      = glob(config.get('Settings', 'dataFiles'))
baseData       = DatasetTI(dataFiles[0])
baseData.printSummary()
ind            = baseData.genSubsetIndices(specs)

baseData['sDataSub'] = baseData['sData'].subsetCols(0)
baseData['oDataSub'] = baseData['oData'].subsetCols(slice(0,10))
kdeData                = baseData['oDataSub'].join(baseData['sDataSub'])
synthetic              = kde.run(kdeData, specs, counts = dotdict({'nGood': N_GOOD, 'nCritical': N_CRITICAL, 'nFail': N_FAIL}))

# Plot everything
plotSyntheticAndReal(synthetic,kdeData.data, 0, 1, config.get('Settings', 'resultDir') + 'pairwisePlot0-1.pdf')
plotSyntheticAndReal(synthetic,kdeData.data, 2, 3, config.get('Settings', 'resultDir') + 'pairwisePlot2-3.pdf')
plotSyntheticAndReal(synthetic,kdeData.data, 4, 5, config.get('Settings', 'resultDir') + 'pairwisePlot4-5.pdf')
plotSyntheticAndReal(synthetic,kdeData.data, 6, 7, config.get('Settings', 'resultDir') + 'pairwisePlot6-7.pdf')
plotSyntheticAndReal(synthetic,kdeData.data, 8, 9, config.get('Settings', 'resultDir') + 'pairwisePlot8-9.pdf')
plotSyntheticAndReal(synthetic,kdeData.data, 9, 10, config.get('Settings', 'resultDir') + 'pairwisePlot9-10.pdf')
plotHistogram(synthetic, kdeData.data, 10, config.get('Settings', 'resultDir') + 'histogramSpec.pdf')





