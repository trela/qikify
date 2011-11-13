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

import sys, os, csv, pandas
import numpy as np
from qikify.helpers import *

class Specs(object):    
    def __init__(self, filename = None, specs=None):
        """Read in specs from `filename` and create {specname: [lsl,usl]} dictionary.
        Alternatively, can provide specs directly.
        """
        if filename is not None:    
            self.specs = pandas.read_csv(filename)
            try:
                self.specs = pandas.DataFrame(self.raw, dtype=float) # try to force floating-point data type
            except Exception, e:
                pass # oh well, we tried
        elif specs is not None:
            self.specs = specs
        else:
            raise Exception('Specs not provided.')
        
        # NaN limits --> +/- infinity
        self.specs.ix[0,np.isnan(self.specs.ix[0,:])] = -np.inf  # lower spec limits
        self.specs.ix[1,np.isnan(self.specs.ix[1,:])] = np.inf   # upper spec limits
        
    def __getitem__(self, key):
        return self.specs[key]
    
    def __str__(self):
        """Print a summary of the specifications.
        """
        output = ''
        for name in self.specs.columns:
           output += RED + '%27s' % name + ENDCOLOR +  ': \t'
           output += ' <> '.join([str(x) for x in self.specs[name].tolist() if not np.isnan(x)]) + '\n'
        return output

    def genCriticalRegion(self, k_i, k_o):
        """Takes specification boundary and generates two boundaries to define 'critical' device 
        region.
        
        Parameters
        ----------
        k_i : Inner critical region multiplier.
        k_u : Outer critical region multiplier.
        """
        self.inner, self.outer = {}, {}
        for name in self.specs.columns:
            lsl, usl   = self.specs[name]
            mu         = np.mean([lsl, usl])
            self.inner[name] = np.array([mu - k_i * abs(mu-lsl), mu + k_i * abs(mu-usl)])
            self.outer[name] = np.array([mu - k_o * abs(mu-lsl), mu + k_o * abs(mu-usl)])
        return self
    
    def computePassFail(self, data):
        """Compare a pandas Series or DataFrame structure to specification limits defined by
        this spec class instance.
        
        Parameters
        ----------
        data : Contains data stored in Series or DataFrame.
        """
        if isinstance(data, pandas.Series):
            lsl, usl = self[data.name]
            return data.apply(lambda x: x >= lsl and x <= usl)
        if isinstance(data, pandas.DataFrame):
            pfMat = pandas.DataFrame(np.ones(data.shape,dtype=bool), columns = data.columns)
            for j in xrange(data.shape[1]):
                lsl, usl = self[data.columns[j]]
                pfMat.ix[:,j] = data.ix[:,j].apply(lambda x: x >= lsl and x <= usl)
            return pfMat
        else:
            raise ValueError('Cannot compare non-pandas data structure.')
            
            
