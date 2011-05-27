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
from numpy import *
from ..helpers.general import *

class DataStruct:
    def __init__(self, names = None, data = None, desc = None, pfMat = None, gnd = None):
        self.names = names
        self.data  = data
        self.desc  = desc
        self.pfMat = pfMat
        self.gnd   = gnd
        self.nrow  = size(data,0)
        self.ncol  = size(data) if (size(data,0) == size(data)) else size(data,1)
        
    def subsetCols(self, cols, desc = None):
        # Numpy won't hstack if data is un-reshaped column vector. So, we reshape if data is column vector.
        # A hack, but not sure how to do this any better at the moment.
        ## TODO: should be replaced with np.atleast_2d()!
        data         = self.data[:,cols]
        if size(data) == size(data,0):
            data = array([self.data[:,cols]]).T
            
        description = self.desc if desc is None else desc
        pfMat       = self.pfMat[:,cols] if (hasattr(self, 'pfMat') and self.pfMat is not None) else None
        gnd         = self.gnd if (hasattr(self, 'gnd') and self.gnd is not None) else None
        return DataStruct(self.names[cols], data, description, pfMat, gnd)

    def subsetRows(self, rows):
        description = self.desc
        pfMat         = self.pfMat[rows,:] if (hasattr(self, 'pfMat') and self.pfMat is not None) else None
        gnd         = self.gnd[rows] if (hasattr(self, 'gnd') and self.gnd is not None) else None
        return DataStruct(self.names, self.data[rows,:], self.desc, pfMat, gnd)

    # Joins the base datastruct with a secondary datastruct (by column)
    def join(self, Secondary, desc = None):
        return DataStruct(names = hstack((self.names, Secondary.names)),
                          data  = hstack((self.data,  Secondary.data)),
                          desc  = desc)

    def joinRows(self, Secondary, desc = None):
        return DataStruct(names = self.names,
                          data  = vstack((self.data, Secondary.data)),
                          desc  = self.desc)
                            
    # Save datasets to files.
    def writeCSV(self, filename):    
        if hasattr(self, 'gnd') and self.gnd is not None:
            dataset = hstack((self.data, self.pfMat, self.gnd.reshape(len(self.gnd),1)))
            names = hstack((self.names, self.names, 'gnd'))
        else:
            dataset = self.data
            names = self.names

        fileh           = open(filename, 'w')
        dataWriter     = csv.writer(fileh)
        dataWriter.writerow(names)
        for row in dataset:
            dataWriter.writerow(row)
        fileh.close()
        print GREEN + 'Saved dataset to ' + filename + ' successfully.' + ENDCOLOR

    # Just print out a summary of the dataset (rows, cols, pass/fail info if available.)
    def __str__(self):
        output = '%-30s  %4d  %4d' % (self.desc, size(self.data,0), size(self.data,1))
        if hasattr(self, 'gnd') and self.gnd is not None:
            output += '\n' + outputPassFail(self.gnd)
        return output
        

