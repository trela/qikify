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
import matplotlib.pyplot as plt

# Compare data to lsl, usl and return +1/-1 label vector
def compareToSpecs(data, lsl, usl):
	result = ones(size(data))
	if ~isnan(lsl):
		result = (data >= lsl)
	if ~isnan(usl):
		result = logical_and(result, data <= usl)
	return bool2symmetric(result)
	
	
# Write mat to filename as a csv.
def csvWriteMatrix(filename, mat):
	out  = csv.writer(open('../data/' + filename, 'wb'))
	for row in mat:
		out.writerow(row)
		
		
# Use dotdict to replace dictionaries. This enables dict.property access.
class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


# Changes True/False data to +1/-1 symmetric.
def bool2symmetric(data):
	return array((data - 0.5) * 2.0, dtype = int)
	
	
def scale(data, scaleDict = None, reverse = False):
	if reverse:
		return (data.copy() * scaleDict.std) + scaleDict.mean
	else:
		if scaleDict is None:
			scaleDict = dotdict({'mean': data.mean(axis = 0), 'std': data.std( axis = 0)})
		return (data.copy() - scaleDict.mean) / scaleDict.std
