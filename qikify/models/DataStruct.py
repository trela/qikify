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
import numpy as np
from qikify.helpers.general import *
from scipy import r_

class DataStruct(np.ndarray):
    def __new__(cls, input_array, names=None, desc=None, pfMat=None, gnd=None):
        obj       = np.asarray(input_array).view(cls)
        obj.names = names
        obj.desc  = desc
        obj.pfMat = pfMat
        obj.gnd   = gnd
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.names = getattr(obj, 'names',  None)
        self.desc  = getattr(obj, 'desc',   None)
        self.pfMat = getattr(obj, 'pfMat',  None)
        self.gnd   = getattr(obj, 'gnd',    None)
        self.indOutliers = getattr(obj, 'indOutliers', None)
        
    # Print out a summary of the dataset (rows, cols, pass/fail info if available.)
    def __str__(self):
        output = '%-30s  %4d  %4d' % (self.desc, self.shape[0], self.shape[1])
        if hasattr(self, 'gnd') and self.gnd is not None:
            output += '\n' + outputPassFail(self.gnd)
        return output
        
    # Save datasets to files.
    def writeCSV(self, filename):    
        # if hasattr(self, 'gnd') and self.gnd is not None:
        #    dataset = hstack((self.data, self.pfMat, self.gnd.reshape(len(self.gnd),1)))
        #    names   = hstack((self.names, self.names, 'gnd'))
        #else:
        #    dataset = self.data
        #    names   = self.names            
        with open(filename, 'w') as f:
            w = csv.writer(f)
            w.writerow(self.names)
            for row in self.view():
                w.writerow(row)
        print GREEN + 'Saved dataset to {0} successfully.'.format(filename) + ENDCOLOR
        
    @property
    def nrow(self):            
        return self.shape[0]
    
    @property
    def ncol(self):
        if self.shape[0] == np.size(self):
            return 1
        else:
            return self.shape[1]
    
    def join(self, secondary):
        out = DataStruct(r_[self, secondary])
        out.names       = getattr(self, 'names',  None)
        out.desc        = getattr(self, 'desc',   None)
        out.pfMat       = getattr(self, 'pfMat',  None)
        out.gnd         = getattr(self, 'gnd',    None)
        out.indOutliers = getattr(self, 'indOutliers', None)
        return out

    # Identify outliers using boundaries with margins determined by k_l / k_u.
    def identifyOutliers(self, specs, ind, k_l = 3, k_u = 3):
        self.computePassFail(specs, ind, outlierFilter=True, k_l=k_l, k_u=k_u)
        return self.indOutliers
        
    # Multipurpose compute pass/fail function. If outlierFilter is False, this function takes
    # the specification performance data, compares each column to spec lsl/usl, and saves
    # pass/fail information for individial specs (pfMat) and the global pass/fail (gnd).
    def computePassFail(self, specs, ind = None, outlierFilter = False, k_l = None, k_u = None):
        pfMat = np.ones(self.shape)
        mu    = np.mean(self,0) if self.ncol > 1 else np.mean(self,0)
     
        # Iterate over columns in pfData     
        for j in xrange(self.ncol):
            # Logical column indices permit skipping some columns
            if type(ind) is dict and ~(ind[dataset][j]):
                continue
            else:
                lsl, usl = specs[self.names[j]] if self.ncol > 1 else specs[self.names]
                if outlierFilter:
                    lsl = mu[j] - k_l * abs(mu[j] - lsl) if not np.isnan(lsl) else np.nan
                    usl = mu[j] + k_u * abs(mu[j] - usl) if not np.isnan(usl) else np.nan
                pfMat[:,j]  = specs.compare(self[:,j], lsl, usl)

        # If we are filtering outliers, return a logical index describing outlier observations.
        # Otherwise, we are computing pass/fail and want to save pfMat and gnd.
        if outlierFilter:
            self.indOutliers = (np.sum(pfMat, 1) == self.ncol)
        else:
            self.pfMat = pfMat
            self.gnd   = bool2symmetric(np.sum(pfMat, 1) == self.ncol)
        return self

    

