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

# 2D Scatterplot of synthetic & actual data.
def plotSample(sData,bData, d1, d2, outFile = None):
	fig, ax = plt.subplots(1)
	ax.scatter(sData[:,d1],sData[:,d2], alpha=0.5, c='r')
	ax.scatter(bData[:,d1],bData[:,d2], alpha=0.5, c='g')
	if outFile is not None:
		fig.savefig(outFile)
	plt.show()


def plotHistograms():
	plt.figure(1)
	for i in range(8):
		ax1 = plt.subplot(3,3,i, axisbg = 'w')
		plt.hist(synData.sData[:,i], 20, alpha=0.5, color='r')
		plt.hist(baseData.sData[:,i], 20, alpha=0.5, color='b')
		plt.grid(True)
		lowerLim = min(hstack((baseData.sData[:,i], synData.sData[:,i])))
		upperLim = max(hstack((baseData.sData[:,i], synData.sData[:,i])))
		plt.xlim([lowerLim, upperLim]) 
	plt.show()	



def pair(data, labels=None):
	""" Generate something similar to R pairs() """
	nVariables = data.shape[1]
	if labels is None:
		labels = ['var%d'%i for i in range(nVariables)]
	fig = plt.figure()
	for i in range(nVariables):
		for j in range(nVariables):
			ax = fig.add_subplot(nVariables, nVariables, i * nVariables + j + 1)
			if i == j:
				ax.hist(data[:,i])
				ax.set_title(labels[i])
			else:
				ax.scatter(data[:,i], data[:,j])
	return fig