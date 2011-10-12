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

import sys, os, csv, gzip
import numpy as np
from qikify.helpers import *
from qikify.models.dotdict import dotdict
from qikify.models.DataStruct import DataStruct

class Dataset(dotdict): 
    def __init__(self, filename=None, hasHeader=True, dataset=None):
        if filename is not None:
            filetype = filename.split('.')[-1]
            if filetype == 'csv':
                # Read dataset column names
                if ( hasHeader ):
                    with open(filename, 'rU') as f:
                        names = np.array(csv.reader(f).next())
                
                # Read numeric data
                rawData  = np.loadtxt(filename, delimiter=',', skiprows=1)
                self.raw = DataStruct(rawData, names=names, desc='Raw dataset.')

            if filetype == 'gz':
                # There's probably a better way to do this.
                with gzip.open(filename, 'rb') as f:
                    raw = f.read().split('\n')
                    if ( hasHeader ):
                        names = np.array(raw.pop(0).split(','))
                    self.raw = [row.split(',') for row in raw]
                    
        if dataset is not None:
            self.raw = DataStruct(dataset.data, names=dataset.names, desc='Raw dataset.')
    
    # Print a summary of the dataset.
    def __str__(self):    
        output = GREEN + \
               '===============================================\n' + \
               'Dataset                         #Rows #Cols    \n' + \
               '===============================================\n' + ENDCOLOR
        for dataset in self.values():
            output += dataset.__str__() + '\n'
        return output
        
''' 
    # Subset the columns of the datasets identified in the ind dictionary.
    # Argument: ind = {'datasetName': columnIndices }
    def subsetCols(self, ind, desc = None):
        for dataset,idx in ind.iteritems():
            self[dataset] = self[dataset][:,idx]
            if self.names:
                self.names = self.names[idx]
        return self

    # Subset the rows of the datasets identified in the ind dictionary.
    # Argument: ind = {'datasetName': rowIndices }
    def subsetRows(self, ind):
        for dataset,idx in ind.iteritems():
            self[dataset] = self[dataset][idx,:]
        return self
        
'''