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

from Dataset import *

class DatasetTI(Dataset):
    
    # Constructor is either based on reading a file or passed in data.
    def __init__(self, filename = None, synData = None, nRetained = None):
        if filename is not None:
            # Call parent class Dataset.__init__() which creates self.datasets and self.datasets.raw.
            super(DatasetTI, self).__init__(filename, hasHeader=True)
            
            # Create child datasets
            self.datasets.sData  = self.datasets.raw.subsetCols(range(739,1106), 'Specification test data.')
            self.datasets.oData  = self.datasets.raw.subsetCols(range(0,739), 'ORBiT test data.')
        else:
            # Call parent class Dataset.__init__() which creates self.datasets.
            super(DatasetTI, self).__init__()
            
            # Create child datasets
            self.datasets.sData  = synData.subsetCols(nRetained, 'Specification test data.')
            self.datasets.oData  = synData.subsetCols(range(0,nRetained), 'ORBiT test data.')


    # Run on first dataset, baseData.
    def genSubsetIndices(self, specs):
        # We will remove all parameters with less than 100 unique values.
        ind = dotdict({'sData': apply_along_axis(lambda x: len(unique(x)) > 100, 0, self['sData'].data),
                       'oData': apply_along_axis(lambda x: len(unique(x)) > 100, 0, self['oData'].data)})

        # Identify all outliers with signatures outside +/- 3 * (spec distance).
        self.identifyOutliers(specs, ind, dataset = 'sData', k_l = 3, k_u = 3)
        
        # Identify specification performances which now always pass.
        self.computePF(specs, ind, dataset = 'sData')
        alwaysPassing = (sum(self['sData'].pfMat[self.indOutliers,:],0) / sum(self.indOutliers) == 1)
        ind.sData  = logical_and(ind.sData, ~alwaysPassing)
        
        self.subsetCols(ind).subsetRows({'sData': self.indOutliers, 'oData': self.indOutliers})
        print self
        return ind

    # Run on every subsequent dataset.
    def clean(self, specs, ind):
        self.subsetCols(ind)
        self.computePF(specs, ind, dataset = 'sData')
        return self
        




