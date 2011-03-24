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

import csv, os, glob, sys, ConfigParser
import matplotlib.pyplot as plt

from numpy import *
from helpers import *
from controllers.kde import KDE, slicesample
from controllers.lsfs import LSFS

# Test KDE.
def testKDE():
	data    = random.multivariate_normal([0,0],[[1,0],[0,1]],1000)
	kde 	= KDE.KDE(data, [[-10,-10],[10,10]])
	synData = kde.run(1000)
	plotSample.plotSample(synData, data, 0,1)


# Test the slicesample() function with a sample pdf 
def testSliceSample():
	# Some crazy distribution
	#f = lambda x: exp(-x**2/2) * (1+(sin(3*x))**2) * (1+(cos(5*x)**2))

	# Standard normal
	#f = lambda x: 1.0 / sqrt(2.0 * pi) * exp(-x**2 / 2 )
	
	# Bivariate normal
	f = lambda x: 1.0 / sqrt(2.0 * pi) * exp(-dot(x,x)**2 / 2 )
	
	# Run slicesample
	initial = array([0,0])
	x = slicesample.slicesample(initial,100,f)

	fig, ax = plt.subplots(1)
	if size(initial) == 1: # univariate distribution
		ax.hist(x, 100)
	else:
		ax.scatter(x[:,0], x[:,1])
	fig.savefig('/Users/nathankupp/Desktop/Figure1.png')
	return x

# Test LSFS constructW function
def testConstructW():
	lsfs = LSFS.LSFS()
	
	# Test case simple
	X = ones((4,4)) + diag(range(1,5))
	gnd = array([-1,1,-1,1])
	lsfs.constructW(X, gnd, bLDA = 1)
	#print lsfs.W
	
	# Test case complex
	X = random.random((10,10))
	gnd = 2 * (random.randint(0,2,10) - 0.5)
	lsfs.constructW(X,gnd, bLDA = 1)
	#print lsfs.W
	
	# Turn off bLDA
	X = ones((4,4)) + diag(range(1,5))
	gnd = array([-1,1,-1,1])
	lsfs.constructW(X, gnd)
	#print lsfs.W
	
	
def testLSFS():
	lsfs = LSFS.LSFS()
	
	X = ones((4,4)) + diag(range(1,5))
	gnd = array([-1,1,-1,1])
	lsfs.run(X, gnd)


if __name__ == "__main__":
	#testKDE()
	#x = testSliceSample()
	#testConstructW()
	testLSFS()
	
	
	
	
	