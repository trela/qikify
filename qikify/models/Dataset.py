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

import sys, os, csv
import numpy as np
from dotdict import dotdict
from DataStruct import *

class Dataset(dotdict): 
    def __init__(self, filename=None, hasHeader=True, dataset=None):
        if filename is not None:
            # Read dataset column names
            if ( hasHeader ):
                fileh          = open(filename, 'rU')
                dataReader     = csv.reader(fileh)
                names          = np.array(dataReader.next())
                fileh.close()
            
            # Read numeric data
            rawData  = np.loadtxt(filename, delimiter=',', skiprows=1)
            self.raw = DataStruct(rawData, names=names, desc='Raw dataset.')
        
        if dataset is not None:
            self.raw = DataStruct(dataset.data, names=dataset.names, desc='Raw dataset.')
        
        
    
    # Identify outliers in the specified dataset using boundaries with margins determined by
    # the k_l and k_u constants.
    def identifyOutliers(self, specs, ind, dataset, k_l = 3, k_u = 3):
        self.computePF(specs, ind, dataset, outlierFilter = True, k_l = k_l, k_u = k_u)

    
    # Multipurpose compute pass/fail function. If outlierFilter is False, this function takes
    # the specification performance data, compares each column to spec lsl/usl, and saves
    # pass/fail information for individial specs (pfMat) and the global pass/fail (gnd).
    def computePF(self, specs, ind = None, dataset = 'raw', outlierFilter = False, k_l = None, k_u = None):
        if dataset not in self.keys():
            raise KeyError('Not a valid dataset.')

        pfData = self[dataset]
        n, p   = size(pfData.data,0), size(pfData.data,1)
        pfMat  = ones((n,p))
        mu        = mean(pfData.data,0) if p > 1 else mean(pfData.data,0)[0]
        
        # Iterate over columns in pfData
        for j in xrange(p):
            # Logical column indices permit skipping some columns
            if type(ind) is dict and ~(ind[dataset][j]):
                continue
            else:
                lsl, usl = specs[pfData.names[j]] if p > 1 else specs[pfData.names]
                if outlierFilter:
                    lsl = mu[j] - k_l * abs(mu[j] - lsl) if not isnan(lsl) else nan
                    usl = mu[j] + k_u * abs(mu[j] - usl) if not isnan(usl) else nan
                pfMat[:,j]  = specs.compareToSpecs(pfData.data[:,j], lsl, usl)

        # If we are filtering outliers, return a logical index describing outlier observations.
        # Otherwise, we are computing pass/fail and want to save pfMat and gnd.
        if outlierFilter:
            self.indOutliers = (sum(pfMat, 1) == p)
        else:
            self[dataset].pfMat = pfMat
            self[dataset].gnd   = bool2symmetric(sum(pfMat, 1) == p)
        return self

    
    # Subset the columns of the datasets identified in the ind dictionary.
    # Argument:
    #    ind = {'datasetName': columnIndices }
    def subsetCols(self, ind, desc = None):
        for dataset in ind.keys():
            if dataset not in self.keys():
                raise KeyError(dataset + ' is not a valid dataset.')
            self[dataset] = self[dataset].subsetCols(ind[dataset], desc = desc)
        return self
        
    # Subset the rows of the datasets identified in the ind dictionary.
    # Argument:
    #    ind = {'datasetName': rowIndices }
    def subsetRows(self, ind):
        for dataset in ind.keys():
            if dataset not in self.keys():
                raise KeyError(dataset + ' is not a valid dataset.')
            self[dataset] = self[dataset].subsetRows(ind[dataset])
        return self
        
    # Join datasets
    def joinRows(self, Secondary):
        newData = self
        for dataset in newData.keys():
            newData[dataset] = newData[dataset].joinRows(Secondary[dataset])
        return newData

    # Print a summary of the dataset.
    def __str__(self):    
        output = RED + \
               '===============================================\n' + \
               'Dataset                         #Rows #Cols    \n' + \
               '===============================================\n' + ENDCOLOR
        for dataset in self.values():
            output += dataset.__str__() + '\n'
        return output




