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
from qikify.helpers import *

class Specs:    
    # Read in specs from `filename` and create {specname: [lsl,usl]} dictionary.
    def __init__(self, filename = None, names = [], specs = {}):
        self.names, self.specs = names, specs
        if filename is not None:
            with open(filename, 'rU') as f:
                reader     = csv.reader(f)
                self.names = reader.next()
                LSL        = reader.next()
                USL        = reader.next()
                for i, limit in enumerate(zip(LSL, USL)):
                    # Use this lambda function because float() fails on empty/non-existent spec limit.
                    lsl, usl = [float(x) if x else float('nan') for x in limit]
                    self.specs[self.names[i]] = np.array([lsl, usl])

    # Compare data to lsl, usl and return +1/-1 label vector
    def compare(self, data, lsl, usl):
        result = np.ones(data.shape,dtype=bool)
        if np.isfinite(lsl): result = np.logical_and(result, data >= lsl)
        if np.isfinite(usl): result = np.logical_and(result, data <= usl)
        return result

    def __getitem__(self, key):
        return self.specs[key]
    
    # Print a summary of the dataset.
    def __str__(self):
        output = ''
        for name in self.names:
           output += RED + '%27s' % name + ENDCOLOR +  ': \t'
           output += ' <> '.join([str(x) for x in self.specs[name].tolist() if not np.isnan(x)]) + '\n'
        return output

    # =============== Partitioned Sampling Methods =============== 
    # Takes specification boundary and generates two boundaries to define 'critical' device region.
    def genCriticalRegion(self, k_i, k_o):
        self.inner, self.outer = {}, {}
        for name in self.specs.keys():
            lsl, usl   = self.specs[name]
            mu         = np.mean([lsl, usl])
            self.inner[name] = np.array([mu - k_i * abs(mu-lsl), mu + k_i * abs(mu-usl)])
            self.outer[name] = np.array([mu - k_o * abs(mu-lsl), mu + k_o * abs(mu-usl)])
        return self

