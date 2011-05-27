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
import scipy.stats as st 

class Charts:
    def percentFormatter(x, pos=0):
         return '%1.2f%%'%(x)

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
    
    def plot_yp_vs_y(yp, y, filename):
        """
        This method plots y predicted vs. y actual on a 45-degree chart.
        """
        fig = plt.figure()
        ax  = fig.add_subplot(111, aspect='equal')
        ax.scatter(yp, y)
        ax.plot([min(y), max(y)], [min(y), max(y)])
        ax.set_xlim((min(y), max(y)))
        ax.set_ylim((min(y), max(y)))
        ax.grid(True)
        plt.savefig(filename, dpi = 150, format='pdf')    
        plt.close()

  
    def qqplot(x, filename):
        values = st.norm.rvs(size=(100,))  # example data 
        fig = plt.figure()                 # set up plot 
        ax = fig.add_subplot(1, 1, 1) 
        osm, osr = st.probplot(x, fit=0, dist='norm')  # compute 
        ax.plot(osm, osr, '.')
        ax.grid(True)
        plt.savefig(filename, dpi = 150, format='pdf')    
        plt.close()


    def pair(data, labels=None):
        """
        Generates something similar to R pairs()
        """
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
        plt.savefig(filename, dpi = 150, format='pdf')    
        plt.close()