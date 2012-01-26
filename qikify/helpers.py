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
import scipy, csv, pandas
from qikify.models.dotdict import dotdict

# Colors for printing to terminal
HEADER   = '\033[95m'
BLUE     = '\033[94m'
GREEN    = '\033[0;32m'
WARNING  = '\033[93m'
RED      = '\033[91m'
ENDCOLOR = '\033[0m'

def outputPassFail(gnd):
    return 'Pass: '+GREEN+str(np.sum(gnd==1))+ENDCOLOR + ' Fail: '+RED+str(np.sum(gnd==0))+ENDCOLOR

def bool2symmetric(data):
    """
    Changes True/False data to +1/-1 symmetric.
    """
    return np.array((data-0.5)*2.0,dtype = int)

def csvWriteMatrix(filename, mat):
    """
    Write mat to filename as a csv.
    """
    out = csv.writer(open(filename, 'wb'))
    for row in np.atleast_2d(mat):
        out.writerow(row)        


def standardize(X, scaleDict = None, reverse = False):
    """Facilitates standardizing data by subtracting the mean and dividing by
    the standard deviation. Set reverse to True to perform the inverse 
    operation.
    
    Parameters
    ----------
    X : numpy ndarray, or pandas.DataFrame
        Data for which we want pareto-optimal front.
    scaleDict: dict, default None
        Dictionary with elements mean/std to control standardization.
    reverse: boolean, default False
        If this flag is set, the standardization will be reversed; e.g.,
        we take a dataset with zero mean and unit variance and change to
        dataset with mean=scaleDict.mean and std=scaleDict.std.
    
    Examples
    --------
    TODO
        
    """
    if reverse:
        return (X * scaleDict.std) + scaleDict.mean
    elif scaleDict is None:
        scaleDict = dotdict({'mean': X.mean(0).tolist(), 'std': X.std(0).tolist()})
        return scaleDict, (X - scaleDict.mean) / scaleDict.std
    else:
        return (X - scaleDict.mean) / scaleDict.std


def zeroMatrixDiagonal(X):
    """Set the diagonal of a matrix to all zeros.
    
    Parameters
    ----------
    X : numpy ndarray
        Matrix on which to zero out the diagonal.
        
    Examples
    --------
    Xp = zeroMatrixDiagonal(X)
    
    """
    return X - np.diag(np.diag(X))


def getParetoFront(data):
    """Extracts the 2D Pareto-optimal front from a 2D numpy array.
    
    Parameters
    ----------
    data : numpy ndarray, or pandas.DataFrame
        Data for which we want pareto-optimal front.
    
    Examples
    --------
    p = getParetoFront(data)
    
    """
    dflags  = np.ones(data.shape[0], dtype=bool)
    for i in xrange(data.shape[0]):
        point = data[i,:]
        for j in xrange(data.shape[0]):
            if i == j:
                continue
            if np.all(point > data[j,:]):
                dflags[i] = False
    return np.array(data[dflags,:])


def is1D(data):
    return data.shape[0] == np.size(data)


def partition(data, threshold=0.5, verbose = False):
    """Partitions data into training and test sets. Assumes the last column of
    data is y.
    
    Parameters
    ----------
    data : numpy ndarray, or pandas.DataFrame
        Data to partition into training and test sets.
    threshold : float
        Determines ratio of training : test.
        
    Examples
    --------
    TODO
        
    """
    
    if data.ndim != 2:
        raise Exception, 'data must be 2-dimensional'

    nrow, ncol = data.shape
    
    # create boolean vector identifying rows in training/test sets.
    index = np.random.sample(nrow)
    train_index = index < threshold
    test_index = index >= threshold
    
    if isinstance(data, pandas.DataFrame):        
        xtrain = data.ix[train_index,:ncol-1]
        ytrain = data.ix[train_index,ncol-1]
        xtest  = data.ix[test_index,:ncol-1]
        ytest  = data.ix[test_index,ncol-1]
    elif isinstance(data, np.ndarray):
        xtrain = data[train_index,:-1]
        ytrain = data[train_index,-1]
        xtest  = data[test_index,:-1]
        ytest  = data[test_index,-1]
    else:
        raise Exception, 'data must be numpy.ndarray or pandas.DataFrame'
    
    if verbose:
        print 'Randomly partitioned data, with threshold={0}'.format(threshold)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('xtrain', *xtrain.shape)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('ytrain', ytrain.size, 1)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('xtest', *xtest.shape)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('ytest', ytest.size, 1)
        
    return xtrain, ytrain, xtest, ytest


def nmse(yhat, y, min_y=None, max_y=None):
    """Calculates the normalized mean-squared error. 
    
    Parameters
    ----------
    yhat : 1d array or list of floats
        estimated values of y
    y : 1d array or list of floats
        true values
    min_y, max_y : float, float
      roughly the min and max; they do not have to be the perfect values of min and max, because
      they're just here to scale the output into a roughly [0,1] range

    Examples
    --------
    nmse = nmse(yhat, y)
    
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


def computeR2(yhat, y):
    """Compute R-squared coefficient of determination:
       R2 = 1 - sum((y_hat - y_test)**2) / sum((y_test - np.mean(y_test))**2)

    Parameters
    ----------
    yhat : 1d array or list of floats -- estimated values of y
    y : 1d array or list of floats -- true values
    
    Examples
    --------
    r2 = computeR2(yhat, y)
    
    """
    #e    = y - yhat              # residuals
    #return 1 - e.var()/y.var() # model R-squared
    #y_bar = np.mean(y)
    #SSReg = sum((yhat - y_bar)**2)
    #SST   = sum((y    - y_bar)**2)
    #return SSReg/SST
    return np.corrcoef(yhat, y)[0,1]**2
    
    

