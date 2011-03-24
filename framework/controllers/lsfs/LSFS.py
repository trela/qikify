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

import sys, os, random, time
from numpy import *
from scipy.sparse import lil_matrix
from scipy.sparse import coo_matrix

from helpers.general import *

# Laplacian score feature selection
class LSFS:
	def run(self, X, gnd):
		self.constructW(X, gnd)
		nSmp	= size(X,0)
		D 		= sum(self.W,1)
		z	 	= dot(D.T,X) * dot(D.T,X) / sum(diag(D))
		D 		= coo_matrix((D,(range(nSmp),range(nSmp))), shape=(nSmp,nSmp))
		DPrime 	= array(sum(multiply(dot(X.T,D.todense()).T, X),1).T - z)[0]
		LPrime 	= array(sum(multiply(dot(X.T,self.W).T, X).T, 1) - z)
		DPrime[DPrime < 1e-12] = 10000
		
		self.Scores = (LPrime/DPrime).T
		self.Ranking = argsort(self.Scores)
		

	# Construct the W matrix used in LSFS
	def constructW(self, fea, gnd, k = 0, t = 1, bLDA = 0, bSelfConnected = 1):
		label 	 = unique(gnd)
		nSamples = len(gnd)
		G 		 = zeros((nSamples,nSamples))
		
		if bLDA:
			for i in xrange(len(label)):
				ind = (gnd==label[i])
				G[ind,ind] = 1.0/sum(ind)
			self.W = G
		else:
			for i in xrange(len(label)):
				ind = nonzero(gnd==label[i])[0]
				D = self.euDist(fea[ind,:], bSqrt = 0)
				D = exp(-D/(2*t**2))
				setSubMat(G, D, ind)
			if not bSelfConnected:
				G = zeroMatrixDiagonal(G)
			self.W = mmax(G,G)


	# Euclidean Distance matrix
	def euDist(self, A,B = None, bSqrt = True):	
		if B is None:
			nSamples = size(A,0)
			aa, ab = sum(A*A,1), dot(A,A.T)
			D = tile(aa,(nSamples,1)).T + tile(aa,(nSamples,1)) - 2*ab
			if bSqrt:
				D = sqrt(D)
			return abs(zeroMatrixDiagonal(mmax(D,D.T)))
		else:
			nSamplesA, nSamplesB = size(A,0), size(B,0)
			aa, bb, ab = sum(A*A,1), sum(B*B,1), dot(A,B.T)
			D = tile(aa,(nSamplesB,1)).T + tile(bb,(nSamplesA,1)) - 2*ab
			if bSqrt:
				D = sqrt(D)
			return abs(D)

