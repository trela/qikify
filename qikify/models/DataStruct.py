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
from ..helpers.general import *


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

    # Print out a summary of the dataset (rows, cols, pass/fail info if available.)
    def __str__(self):
        output = '%-30s  %4d  %4d' % (self.desc, self.shape[0], self.shape[1])
        if hasattr(self, 'gnd') and self.gnd is not None:
            output += '\n' + outputPassFail(self.gnd)
        return output
        
    # Save datasets to files.
    def writeCSV(self, filename):    
        #if hasattr(self, 'gnd') and self.gnd is not None:
        #    dataset = hstack((self.data, self.pfMat, self.gnd.reshape(len(self.gnd),1)))
        #    names   = hstack((self.names, self.names, 'gnd'))
        #else:
        #    dataset = self.data
        #    names   = self.names            
        with open(filename, 'w') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(self.names)
            for row in self.view():
                csvWriter.writerow(row)
        print GREEN + 'Saved dataset to ' + filename + ' successfully.' + ENDCOLOR

    def nrow(self):
        return self.shape[0]

    def ncol(self):
        return self.shape[1]
