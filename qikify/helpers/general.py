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
import scipy

# Colors for printing to terminal
HEADER   = '\033[95m'
BLUE     = '\033[94m'
GREEN    = '\033[92m'
WARNING  = '\033[93m'
RED      = '\033[91m'
ENDCOLOR = '\033[0m'

def outputPassFail(gnd):
    return 'Pass: '  + GREEN + str(sum(gnd ==  1)) + ENDCOLOR + ' Fail: ' + RED + str(sum(gnd == -1)) + ENDCOLOR

def bool2symmetric(data):
    """
    Changes True/False data to +1/-1 symmetric.
    """
    return np.array((data - 0.5) * 2.0, dtype = int)

def csvWriteMatrix(filename, mat):
    """
    Write mat to filename as a csv.
    """
    out  = csv.writer(open(filename, 'wb'))
    for row in np.atleast_2d(mat):
        out.writerow(row)        
    
class dotdict(dict):
    """
    Use dotdict to replace dictionaries. This enables dict.property access.
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


def scale(data, scaleDict = None, reverse = False):
    """
    Facilitates standardizing data by subtracting the mean and dividing by
    the standard deviation. Set reverse to True to perform the inverse 
    operation.
    """
    if reverse:
        return (data * scaleDict.std) + scaleDict.mean
    elif scaleDict is None:
        scaleDict = dotdict({'mean': data.mean(axis = 0), 'std': data.std( axis = 0)})
        return scaleDict, (data - scaleDict.mean) / scaleDict.std
    else:
        return (data - scaleDict.mean) / scaleDict.std

def zeroMatrixDiagonal(X):
    """
    Set the diagonal of a matrix to all zeros
    """
    return X - np.diag(np.diag(X))

def _strictly_dominated(x,y):
    strictly_dominated = False
    if (x[0] > y[0]) and (x[1] > y[1]):
        strictly_dominated = True
    return strictly_dominated

def getParetoFront(data):
    """
    Extracts the 2D Pareto-optimal front from a 2D numpy array
    """
    dflags  = np.zeros(data.shape[0], dtype=bool)
    for i in xrange(data.shape[0]):
        point = data[i,:]
        pareto_optimal = True
        for j in xrange(data.shape[0]):
            if i == j:
                continue
            if _strictly_dominated(point, data[j,:]):
                dflags[i] = True
    return np.array(data[~dflags,:])


class statHelpers:
    def nmse(self, yhat, y, min_y=None, max_y=None):
        """
        @description
            Calculates the normalized mean-squared error. 
        
        @arguments
            yhat -- 1d array or list of floats -- estimated values of y
            y -- 1d array or list of floats -- true values
            min_y, max_y -- float, float -- roughly the min and max; they
              do not have to be the perfect values of min and max, because
              they're just here to scale the output into a roughly [0,1] range
        
        @return
            nmse -- float -- normalized mean-squared error
        """
        #base case: no entries
        if len(yhat) == 0:
            return 0.0
        
        #base case: both yhat and y are constant, and same values
        if (max_y == min_y) and (max(yhat) == min(yhat) == max(y) == min(y)):
            return 0.0
        
        #main case
        assert max_y > min_y, 'max_y=%g was not > min_y=%g' % (max_y, min_y)
        yhat_a, y_a = np.asarray(yhat), np.asarray(y)
        y_range = float(max_y - min_y)
        try:
            result = np.sqrt(np.mean(((yhat_a - y_a) / y_range) ** 2))
            if scipy.isnan(result):
                return np.Inf
            return result
        except ValueError:
            print 'Invalid result %d' % (result)
            return np.Inf


    def computeCorrCoefs(self, X,y):
        '''
        Returns the correlation coefficients between X and y, 
        along with the arg-sorted indices of ranked most-correlated X-to-y vars.
        '''
        cc = []
        for i in xrange(X.shape[1]):
            cc.append(np.corrcoef(X[:,i], y)[0,1])
        return np.array(cc), np.argsort(-abs(np.array(cc)))

    def computeR2(self, yp, y):
        """
        Compute R-squared coefficient of determination.
        R2 = 1 - sum((model.predict(X_test) - y_test)**2) / sum((y_test - np.mean(y_test))**2)
        """
        e    = y - yp              # residuals
        return 1 - e.var()/y.var() # model R-squared


