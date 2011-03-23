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

import csv, os, glob, numpy, sys, ConfigParser
from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from scikits.learn.metrics import confusion_matrix
from scikits.learn.svm import SVC
import matplotlib.pyplot as plt

from modeling.dataset import Dataset, Dataset_TI, Specs
from modeling.helpers import *
from modeling.kde import KDE, plotSample, slicesample


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



if __name__ == "__main__":
	testKDE()
	#x = testSliceSample()
	
	
	
	
	
	