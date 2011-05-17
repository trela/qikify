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

# Colors for printing to terminal
HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
RED = '\033[91m'
ENDCOLOR = '\033[0m'


def outputPassFail(gnd):
    return 'Pass: '  + GREEN + str(sum(gnd ==  1)) + ENDCOLOR + ' Fail: ' + RED + str(sum(gnd == -1)) + ENDCOLOR

def printPassFail(gnd):
    print outputPassFail(gnd)
    
# Changes True/False data to +1/-1 symmetric.
def bool2symmetric(data):
    return array((data - 0.5) * 2.0, dtype = int)

    
# Write mat to filename as a csv.
def csvWriteMatrix(filename, mat):
    out  = csv.writer(open(filename, 'wb'))
    for row in mat:
        out.writerow(row)
        
        
# Use dotdict to replace dictionaries. This enables dict.property access.
class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


# Extracts a subset of a dictionary.
def extract(keys, d):
    return dict((k, d[k]) for k in keys if k in d)


# Facilitates standardizing data by subtracting the mean and dividing by
# the standard deviation. Set reverse to True to perform the inverse 
# operation.
def scale(data, scaleDict = None, reverse = False):
    if reverse:
        return (data * scaleDict.std) + scaleDict.mean
    else:
        if scaleDict is None:
            scaleDict = dotdict({'mean': data.mean(axis = 0), 'std': data.std( axis = 0)})
        return (data - scaleDict.mean) / scaleDict.std


# Set the diagonal of a matrix to all zeros
def zeroMatrixDiagonal(X):
    return X - diag(diag(X))


# Returns a matrix which is the elementwise maximum of two matrices X and Y
mmax = vectorize(lambda x,y: max(x,y), otypes = [float32])


