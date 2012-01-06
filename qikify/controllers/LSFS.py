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
from scipy.spatial.distance import pdist, squareform
from qikify.helpers import *
import pandas

# Laplacian score feature selection
class LSFS(object):
    def run(self, Xin, gnd):
        """Run LSFS. Arguments are `dataset`, a DataStruct object, and gnd, a 
        pass/fail vector of the same size. Based on definition from paper:
        
         \sum_{ij} (f_r^i - f_r^j) * S_{ij}
         ----------------------------------
                      sigma_2
        
        Now, with newfangled (albeit hacky) support for pandas DataFrames!
        TODO: Eventually, it'd be nice to maintain col names w/ Xin so we
        can add plot method to plot scores vs. column names.
        """
        if isinstance(Xin, pandas.DataFrame):
            X = Xin.as_matrix()
        else:
            X = Xin
        
        nSmp = X.shape[0]
        if nSmp != len(gnd): 
            raise Exception("Data and gnd do not have matching sizes")
        
        _, X = standardize(X)
        
        # Per LSFS paper, S_ij = exp(-||x_i - x_j||^2 / t). I've found that
        # t = ncol(X) to be a suitable choice; anything on that order should 
        # work just fine.
        S          = self.constructS(X, gnd, t=X.shape[1]) 
                   
        D          = sum(S,1)
        z          = dot(D,X) * dot(D,X) / sum(diag(D))        
        LPrime     = sum((dot(X.T,S).T * X).T,1) - z
        DPrime     = sum(dot(X.T,diag(D)).T * X,0) - z
        
        # Remove trivial solutions
        DPrime[DPrime < 1e-12] = inf
        
        # Compute and retain Laplacian scores and rankings
        self.Scores    = (LPrime/DPrime).T
        self.Ranking   = argsort(-self.Scores)
        
        del S  # Clean up to save memory
        return self
        
    def threshold(self, T_L):
        self.subset    = self.Scores > T_L
        self.nRetained = int(sum(self.subset))
        print 'LSFS: retained', GREEN+str(self.nRetained)+ENDCOLOR, 'parameters.'
        return self.subset

    # Construct the W matrix used in LSFS
    def constructS(self, X, gnd, k = 0, t = 1, bLDA=False, bSelfConnected=True):
        label = unique(gnd)
        G     = zeros((len(gnd),len(gnd)))
        if bLDA:
            for i in xrange(len(label)):
                ind = (gnd==label[i])
                G[ix_(ind,ind)] = 1.0/sum(ind)
            return G
        else:
            for i in xrange(len(label)):
                ind = nonzero(gnd==label[i])[0]
                D   = squareform(pdist(X[ind,:], 'sqeuclidean'))  # D_ij = ||x_i - x_j||^2
                S   = exp(-D/t)                                   # Per LSFS paper, exp(-||x_i - x_j||^2 / t)
                self._setSubMat(G, S, ind)                         
            if not bSelfConnected:
                G = zeroMatrixDiagonal(G)
            return self._genMaxMatrix(G)
        print 'LSFS: Construction of W matrix complete.'

    def _setSubMat(self, X, D, ind):
        """Set a submatrix of X defined by the index ind to values in D. 
        That is:
                 [0, 0, 0]
             X = [0, 0, 0]   D = [1 2] ind = [0 1]
                 [0, 0, 0]       [3 4]
        Gives:
                 [1, 2, 0]
             X = [3, 4, 0]
                 [0, 0, 0]
        """
        for i, row in enumerate(ind):
            X[row,ind] = D[i,:]

    def _genMaxMatrix(self, A):
        """Takes a square matrix A and computes max(A, A')"""
        ind = (A.T - A) > 0
        A[ind] = A.T[ind]
        return A

