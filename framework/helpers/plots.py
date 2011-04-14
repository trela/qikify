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
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import FuncFormatter
import pylab

def percentFormatter(x, pos=0):
     return '%1.2f%%'%(x)

def plotLSFSThresholds(results, filename, thresholds):
    results[:,1] *= 10000
    results[:,2] *= 10000
    teMeans = []
    ylMeans = []
    teMins = []
    ylMins = []
    teMaxs = []
    ylMaxs = []
    for threshold in thresholds:
        rowIndex = (results[:,0] == threshold)
        teMeans.append(mean(results[rowIndex,1]))
        ylMeans.append(mean(results[rowIndex,2]))
        teMins.append(min(results[rowIndex,1]))
        ylMins.append(min(results[rowIndex,2]))
        teMaxs.append(max(results[rowIndex,1]))
        ylMaxs.append(max(results[rowIndex,2]))
    bestThresh = thresholds[argmin(teMeans)]
    prop = matplotlib.font_manager.FontProperties(size=10)
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    
    # Mean TE/YL
    ax.plot(thresholds, teMeans,'k-')
    ax.plot(thresholds, ylMeans,'k--')
    
    # Showing choice of threshold via TE
    ax.plot([bestThresh, bestThresh], [0, min(teMeans)],'k-', alpha=1, linewidth=0.5, label='_nolegend_')
    ax.plot([0, bestThresh], [min(teMeans), min(teMeans)],'k-', alpha=1, linewidth=0.5, label='_nolegend_')
    ax.fill_between([0, bestThresh], [0,0], [min(teMeans), min(teMeans)], facecolor='black', alpha=0.2, label='_nolegend_')
    
    # Error range on TE/YL
    ax.fill_between(thresholds, teMins, teMaxs, facecolor='red', alpha=0.5)
    ax.fill_between(thresholds, ylMins, ylMaxs, facecolor='green', alpha=0.5)
    
    leg = ax.legend((r"$T_E$", r"$Y_L$"), 'best', shadow=True, prop = prop)
    ax.grid(True)
    #ax.set_title('Test Escapes and Yield Loss vs. LSFS Threshold')
    plt.xlabel(r"$\tau_{L}$")
    plt.ylabel("Test Metric Values (PPM)")
    #ax.yaxis.set_major_formatter(FuncFormatter(percentFormatter))
    ax.set_xlim((min(thresholds),max(thresholds)))
    plt.savefig(filename, dpi = 150, format='pdf')    
    plt.close()


def plotTEYL(error, errorSyn, filename):
    prop = matplotlib.font_manager.FontProperties(size=10)
    [teSyn, ylSyn] = mean(errorSyn,0)
    [teActual, ylActual] = mean(error,0)
    nWafers = size(error,0)
    fig = pylab.figure()
    
    ax = fig.add_subplot(211)
    ax.plot(error[:,0],'k-')
    ax.plot([0,nWafers],[teSyn, teSyn],'g--')
    ax.plot([0,nWafers],[teActual, teActual],'k-')
    leg = ax.legend((r"$T_E$", r"$\hat{T}_E$", r"$\bar{T}_E$"), 'best', shadow=True, prop = prop)
    ax.grid(True)
    ax.set_title('Test Escapes')
    
    ax = fig.add_subplot(212)
    ax.plot(error[:,1],'k-',
            [0,nWafers],[ylSyn, ylSyn],'g--',
            [0,nWafers],[ylActual, ylActual],'k-')
    leg = ax.legend((r"$Y_L$", r"$\hat{Y}_L$", r"$\bar{Y}_L$"), 'best', shadow=True, prop = prop)
    ax.grid(True)
    ax.set_title('Yield Loss')
    plt.savefig(filename, dpi = 150, format='pdf')    
    plt.close()


# 2D Scatterplot of synthetic & actual data.
def plotSyntheticAndReal(sData, bData, d1, d2, filename):
    fig, ax = plt.subplots(1)
    ax.scatter(sData[:,d1],sData[:,d2], alpha=0.5, c='r')
    ax.scatter(bData[:,d1],bData[:,d2], alpha=0.5, c='g')
    plt.savefig(filename, dpi = 150, format='pdf')    
    plt.close()


def plotHistogram(sData, bData, i, filename):
    fig, ax = plt.subplots(1)
    ax.hist(sData[:,i], 50, normed=True, alpha=0.5, color='r')
    ax.hist(bData[:,i], 50, normed=True, alpha=0.5, color='g')
    ax.grid(True)
    plt.savefig(filename, dpi = 150, format='pdf')    
    plt.close()    



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
