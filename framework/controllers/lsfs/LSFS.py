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

import matplotlib.pyplot as plt
from numpy import *
from scipy.sparse import lil_matrix
from scipy.sparse import coo_matrix

from helpers.general import *

# Laplacian score feature selection
class LSFS:
            
    # Run LSFS. Arguments are `dataset`, a DataStruct object, and gnd, a pass/fail vector of the same size.
    # Based on paper equation:
    #
    # \sum_{ij} (f_r^i - f_r^j) * S_{ij}
    # ----------------------------------
    #              sigma_2
    #
    def run(self, X, gnd):
        if not (size(X,0) == len(gnd)): raise Exception( "Data and gnd do not have matching sizes" )
        
        self.constructW(scale(X), gnd, t = size(X,1), bLDA = False)
        
        nSmp    = size(X,0)
        D         = sum(self.W,1)
        z         = dot(D,X) * dot(D,X) / sum(diag(D))
        D         = coo_matrix((D,(range(nSmp),range(nSmp))), shape=(nSmp,nSmp))
        DPrime     = array(sum(multiply(dot(X.T,D.todense()).T, X),0) - z)[0]
        LPrime     = array(sum(multiply(dot(X.T,self.W).T, X).T, 1) - z)
        DPrime[DPrime < 1e-12] = 10000
        
        # Compute and retain Laplacian scores and rankings
        self.Scores    = (LPrime/DPrime).T
        self.Ranking   = argsort(self.Scores)
        
        # Clean up to save memory
        del self.W
        
        return self
        
    def subset(self, thresh):    
        self.Subset    = self.Scores < thresh
        self.nRetained = sum(self.Subset)
        print 'LSFS: retained', GREEN+str(self.nRetained)+ENDCOLOR, 'parameters.'
        return self.Subset


    # Construct the W matrix used in LSFS
    def constructW(self, fea, gnd, k = 0, t = 1, bLDA = 0, bSelfConnected = 1):
        label      = unique(gnd)
        nSamples = len(gnd)
        G          = zeros((nSamples,nSamples))
        if bLDA:
            for i in xrange(len(label)):
                ind = (gnd==label[i])
                G[ix_(ind,ind)] = 1.0/sum(ind)
            self.W = G
        else:
            for i in xrange(len(label)):
                ind = nonzero(gnd==label[i])[0]
                D = self.euDist(fea[ind,:], bSqrt = False)
                D = exp(-D/t)
                self.setSubMat(G, D, ind)
            if not bSelfConnected:
                G = zeroMatrixDiagonal(G)
            self.W = self.genMaxMatrix(G)
        print 'LSFS: Construction of W matrix complete.'
        
    # Euclidean Distance matrix
    def euDist(self, A,B = None, bSqrt = True):
        if B is None:
            nSamples = size(A,0)
            D = tile(sum(A*A,1),(nSamples,1))
            D = D.T + D
            D -= 2*dot(A,A.T)
            if bSqrt:
                D = sqrt(D)
            return abs(zeroMatrixDiagonal(self.genMaxMatrix(D)))
        else:
            nSamplesA, nSamplesB = size(A,0), size(B,0)
            aa, bb, ab = sum(A*A,1), sum(B*B,1), dot(A,B.T)
            D = tile(aa,(nSamplesB,1)).T + tile(bb,(nSamplesA,1)) - 2*ab
            if bSqrt:
                D = sqrt(D)
            return abs(D)


    # Set a submatrix to values in D. That is:
    #          [0, 0, 0]
    #    X = [0, 0, 0]  D = [1 2] ind = [0 1]
    #          [0, 0, 0]       [1 2]
    # Gives:
    #
    #          [1, 2, 0]
    #    X = [1, 2, 0]
    #          [0, 0, 0]
    def setSubMat(self, X, D, ind):
        for i, row in enumerate(ind):
            X[row,ind] = D[i,:]

    # Takes a square matrix A and computes max(A, A')
    def genMaxMatrix(self, A):
        ind = (A.T - A) > 0
        A[ind] = A.T[ind]
        return A

    def plotScores(self, filename):
        plt.plot(self.Scores[self.Ranking], 'k-')
        plt.grid(True)
        plt.xlabel('Features Retained')
        plt.ylabel('Laplacian Score')
        plt.savefig(filename, dpi = 150, format='pdf')
        plt.close()
        return self