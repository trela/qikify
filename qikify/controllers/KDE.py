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

import sys, os, random, pandas
import numpy as np
from scipy.special import gamma

from qikify.helpers import *
from qikify.models.Specs import Specs
from slicesample import * 

class KDE(object):

    def run(self, X, specs = None, nSamples = 0, counts = None, a = 0, bounds = None):
        """Primary execution point. Run either standard KDE or class-membership based KDE. If 
        any of the class-membership based KDE arguments are set, it will be run instead of 
        standard KDE.
                
        Parameters
        ----------
        X : Contains data stored in a pandas DataFrame.
        nSamples : The number of samples to generate.
        specs  : (optional) If using partitioned sampling, boundaries defining pass/critical/fail
                 subspaces must be provided.
        counts : (optional) If using partitioned sampling, counts dictionary must be provided, with
                 three keys: nGood, nCritical, nFail.
                 
        """
        self.n, self.d = X.shape
        self.specs     = specs
        self.columns   = getattr(X, 'columns', None)
        
        # Normalize data/bounds        
        self.scaleFactors, self.Xn = scale(X)
        self.bounds                = scale(np.array([X.min(0), X.max(0)]), self.scaleFactors)
        if bounds is not None:
            self.bounds = scale(bounds, self.scaleFactors)
            
        # Select bandwidth for Epanechnikov kernel (Rule of Thumb, see Silverman, p.86)
        self.b       = 0.8                     # Default bandwidth scaling factor
        self.c_d     = 2.0* pow( np.pi, (self.d/2.0) ) / ( self.d * gamma(self.d/2) )
        self.h       = self._compute_h(self.n, self.d, self.c_d, self.b)
        self._setBandwithFactors(a)
        
        # Generate samples
        if counts is None:
            return self._genSamples(nSamples)
        else:
            print 'KDE: Running on dataset of size n:', self.n, 'd:', self.d,'and generating', sum(counts.values()), 'samples.'
            self._genSpecLimits(X, specs)
            return self._genPartitionedSamples(counts)
        

    # =============== Private class methods =============== 
    # Default method of generating device samples
    def _genSpecLimits(self, X, specs):
        """We convert spec lims to arrays so spec compare during device sample generation is fast."""
        self.inner = zeros((2,X.shape[1]))
        self.outer = zeros((2,X.shape[1]))
        for i, name in enumerate(X.columns):
            self.inner[:,i] = self.specs.inner[name] if name in self.specs.inner.keys() else [-np.inf, np.inf]
            self.outer[:,i] = self.specs.outer[name] if name in self.specs.outer.keys() else [-np.inf, np.inf]

    def _genSamples(self, nSamples):
        """Generate KDE samples."""
        Sn = vstack([ self._genSample() for _ in xrange(nSamples) ])
        return pandas.DataFrame(scale(Sn, self.scaleFactors, reverse = True), columns = self.columns)
      
    def _genPartitionedSamples(self, counts):
        """Generates nCritical critical devices, nGood good devices, nFail failing devices,
        with each region defined by specs.inner / specs.outer."""

        # Initialize arrays for speed
        Sg, Sc, Sf = zeros((counts.nGood, self.d)), zeros((counts.nCritical, self.d)), zeros((counts.nFail, self.d))
        ng, nc, nf = 0, 0, 0
        
        thresh = 0.02
        while ( ng+nc+nf < sum(counts.values()) ):
            sample = scale(self._genSample(), self.scaleFactors, reverse = True)
            if self.isGood(sample) and ng < counts.nGood:
                Sg[ng,:] = sample
                ng += 1
            if self.isFailing(sample) and nf < counts.nFail:
                Sf[nf,:] = sample
                nf += 1
            if self.isCritical(sample) and nc < counts.nCritical:
                Sc[nc,:] = sample
                nc += 1      
            
            # Prints # generated in each category so we can monitor progress, since this can take a while :) 
            if (1.0*(ng+nc+nf)/sum(counts.values())) > thresh:
                print 'Ng:%i/%i Nc:%i/%i Nf:%i/%i' % (ng,counts.nGood,nc,counts.nCritical,nf,counts.nFail)
                thresh += 0.02
        print 'Non-parametric density estimation sampling complete.'
        return pandas.DataFrame(vstack((Sc,Sg,Sf)), columns=self.columns)


    def _genSample(self):
        """Generate a single sample using algorithm in Silverman, p. 143"""
        j = random.randint(self.n)
        e = slicesample(zeros(self.d), 1, self.K_e)
        s = self.Xn.ix[j,:] + self.h * self.lambdas[j] * e

        # Use mirroring technique to deal with boundary conditions.
        # Perhaps we should consider applying boundary kernels here...
        for k in xrange(self.d):
            if (s[k] < self.bounds[0,k]):
                s[k] = self.bounds[0,k]+abs(self.bounds[0,k]-s[k])
            if (s[k] > self.bounds[1,k]):
                s[k] = self.bounds[1,k]-abs(self.bounds[1,k]-s[k])
        return s

    def _setBandwithFactors(self, a):
        """Estimate local bandwidth factors lambda"""
        self.lambdas = ones(self.n)
        if (a > 0):
            B = [log10(self.f_pilot(self.Xn.ix[i,:], self.Xn)) for i in xrange(self.n)] 
            g = pow(10,sum(B)/self.n)
            self.lambdas = [pow(self.f_pilot(self.Xn.ix[i,:], self.Xn)/g,-a) for i in xrange(self.n)]

    def _compute_h(self, n, d, c_d, b):
        """Computed here seperately to preserve readability of the equation."""
        return b * pow( (8/c_d*(d+4) * pow(2*sqrt(np.pi),d) ), (1.0/(d+4))) * pow(n,-1.0/(d+4))

    def K_e(self, t):
        """Epanechnikov kernel"""
        return (self.d+2)/self.c_d*(1-dot(t,t))/2 if dot(t,t) < 1 else 0

    def f_pilot(self, x, Xn):
        """Compute pilot density point estimate f(x)"""
        A = [self.K_e((x-Xn.ix[i,:])/self.h) for i in xrange(n)]
        return (pow(self.h,-d)*sum(A))/n

    # =============== Partitioned Sampling Methods =============== 
    def isGood(self, sample):
        return all(sample > self.inner[0,:]) and all(sample < self.inner[1,:])

    def isCritical(self, sample):
        return not (self.isGood(sample) or self.isFailing(sample))

    def isFailing(self, sample):
        return (any(sample < self.outer[0,:]) or any(sample > self.outer[1,:]))

