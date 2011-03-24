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

from numpy import *

class DataStruct:
	def __init__(self, names = None, data = None, desc = None, pfMat = None, gnd = None):
		self.names = names
		self.data  = data
		self.desc  = desc
		self.pfMat = pfMat
		self.gnd   = gnd

	def subsetCols(self, cols, desc = None):
		description = self.desc if desc is None else desc
		pfMat       = self.pfMat[:,cols] if (hasattr(self, 'pfMat') and self.pfMat is not None) else None
		gnd 		= self.gnd if (hasattr(self, 'gnd') and self.gnd is not None) else None
		return DataStruct(self.names[cols], self.data[:,cols], description, pfMat, gnd)

	def subsetRows(self, rows):
		description = self.desc
		pfMat 		= self.pfMat[rows,:] if (hasattr(self, 'pfMat') and self.pfMat is not None) else None
		gnd 		= self.gnd[rows] if (hasattr(self, 'gnd') and self.gnd is not None) else None
		return DataStruct(self.names, self.data[rows,:], self.desc, pfMat, gnd)
