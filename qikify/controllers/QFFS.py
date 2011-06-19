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

import numpy as np

from ..helpers.general import *

###############################################################################
# Feature Selection

class QFFS:
    def __init__(self):
        self.qfsh = statHelpers()
        
    def run(self, X, y, n_features=10, intercept=True, method='univariate'):
        """Do feature selection on the basis of correlation coefficients.
        
        Parameters
        ----------
        X : numpy array of shape [n_samples,n_features]
            Training data

        y : numpy array of shape [n_samples]
            Target values

        n_features : int, optional
            Number of features to retain

        intercept : bool, optional
            Whether the first column is an all-constant intercept and 
            should be excluded

        method : string, optional
            Determines the feature selection method to use.

        Returns
        -------
        features : The X column indices to retain.

        Notes
        -----
        We typically exclude the first column since it is the intercept
        all-constant column.
        """
        if method=='univariate':
            if intercept:
                cc, cs = self.qfsh.computeCorrCoefs(X[:,1:],y)
                return np.concatenate(([0],cs[0:n_features] + 1))
            else:
                cc, cs = self.qfsh.computeCorrCoefs(X,y)
                return cs[0:n_features]
              
                
                
                
                
                