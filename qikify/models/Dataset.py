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

import sys, os, csv, gzip, StringIO, pandas
import numpy as np

from qikify.helpers import *
from qikify.models.dotdict import dotdict

class Dataset(dotdict): 
    """This class is the fundamental data structure of the Qikify framework.
    """
    def __init__(self, filename=None, dataset=None):
        if filename is not None:
            filetype = filename.split('.')[-1]
            
            if filetype == 'csv':
                self.raw = pandas.read_csv(filename)
                self.raw.desc = 'Raw data from input file.'

            if filetype == 'gz':
                with gzip.open(filename, 'r') as f:
                    self.raw = pandas.read_csv(StringIO.StringIO(f.read()))
                    
        if dataset is not None:
            self.raw = dataset
    
    def __str__(self):    
        """Print a summary of the dataset."""
        output = GREEN + \
               '===============================================\n' + \
               'Dataset                         #Rows #Cols    \n' + \
               '===============================================\n' + ENDCOLOR
        for key in self.keys():
            output += '%-30s %5d %5d\n' % (key, self[key].shape[0], self[key].shape[1])
        return output
    
    
