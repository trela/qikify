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
import csv, pandas
import numpy as np
from qikify.helpers import *
from scipy import r_

class DataFrame(pandas.DataFrame):
    """Not used, for now. Need to implement subclass ix() property method 
    correctly before this is worth pursuing... right now, indexing a
    qikify.DataFrame with ix will return a pandas.DataFrame instance.
    """
    def __init__(self, pfMat=None, gnd=None, **kwargs):
        super(DataFrame, self).__init__(**kwargs)
        self.pfMat = pfMat
        self.gnd   = gnd
        
    def __str__(self):
        """Print out a summary of the dataset (rows, cols, pass/fail info if available.)"""
        output = '%-30s  %5d  %5d' % (self.desc, self.shape[0], self.shape[1])
        if hasattr(self, 'gnd') and self.gnd is not None:
            output += '\n' + outputPassFail(self.gnd)
        return output

    @property
    def nrow(self):            
        return self.shape[0]
    
    @property
    def ncol(self):
        return 1 if is1D(self) else self.shape[1]
    
    @property
    def ix(self):
        pass
