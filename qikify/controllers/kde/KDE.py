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

import sys, os, random
import numpy as np
from scipy.special import gamma

from helpers.general import *
from models.Specs import Specs
from models.DataStruct import DataStruct

from slicesample import * 

class KDE:
    # Primary execution point. Run either standard KDE or class-membership based KDE. If 
    # any of the class-membership based KDE arguments are set, it will be run instead of 
    # standard KDE.
    def run(self, dataset, specs = None, nSamples = 0, counts = None, a = 0, bounds = None):
        self.n, self.d = dataset.shape
        self.specs     = specs
        self.names     = dataset.names

        # Select bandwidth for Epanechnikov kernel (Rule of Thumb, see Silverman, p.86)
        self.b       = 0.8                     # Default bandwidth scaling factor
        self.c_d     = 2.0* pow( pi, (self.d/2.0) ) / ( self.d * gamma(self.d/2) )
        self.h       = self.compute_h(self.n, self.d, self.c_d, self.b)
        self.setBandwithFactors(a)
        
        # Normalize data/bounds
        self.scaleFactors       = dotdict({'mean': dataset.mean(axis = 0), 'std': dataset.std(axis = 0)})
        self.datan              = scale(dataset, self.scaleFactors)
        self.bounds             = scale(array([dataset.min(axis=0), dataset.max(axis=0)]), self.scaleFactors)
        if bounds is not None:
            self.bounds         = scale(bounds, self.scaleFactors)

        # Generate samples
        if counts is None:
            return self.genSamples(nSamples)
        else:
            print 'KDE: Running on dataset of size n:', self.n, 'd:', self.d,'and generating', sum(counts.values()), 'samples.'
            self.genSpecLimits(dataset, specs)
            return self.genPartitionedSamples(counts)


    # We convert spec lims to arrays so spec compare during device sample generation is fast.
    def genSpecLimits(self, dataset, specs):
        self.inner = zeros((2,dataset.ncol))
        self.outer = zeros((2,dataset.ncol))
        for i, name in enumerate(dataset.names):
            self.inner[:,i] = self.specs.inner[name] if name in self.specs.inner.keys() else [-inf, inf]
            self.outer[:,i] = self.specs.outer[name] if name in self.specs.outer.keys() else [-inf, inf]


    # =============== Private class methods =============== 
    # Default method of generating device samples
    def genSamples(self, nSamples):
        Sn = vstack([ self.genSample() for _ in xrange(nSamples) ])
        return DataStruct(names = self.names, data = scale(Sn, self.scaleFactors, reverse = True))
      
    # Generates Ngc critical devices, Ng good devices, Nf failing devices.
    def genPartitionedSamples(self, counts):
        # Initialize arrays for speed
        Sg, Sc, Sf = zeros((counts.nGood, self.d)), zeros((counts.nCritical, self.d)), zeros((counts.nFail, self.d))
        ng, nc, nf = 0, 0, 0

        thresh = 0.02
        while ( ng+nc+nf < sum(counts.values()) ):
            sample = scale(self.genSample(), self.scaleFactors, reverse = True)
            if self.isGood(sample) and ng < counts.nGood:
                Sg[ng,:] = sample
                ng += 1
            if self.isFailing(sample) and nf < counts.nFail:
                Sf[nf,:] = sample
                nf += 1
            if self.isCritical(sample) and nc < counts.nCritical:
                Sc[nc,:] = sample
                nc += 1       
            if (1.0*(ng+nc+nf)/sum(counts.values())) > thresh:
                print 'Ng:%i/%i Nc:%i/%i Nf:%i/%i' % (ng,counts.nGood,nc,counts.nCritical,nf,counts.nFail)
                thresh += 0.02
        print 'Synthetic data generation complete.'
        return DataStruct(vstack((Sc,Sg,Sf)), names=self.names)


    # Generate a single device sample, use algorithm in Silverman, p. 143
    def genSample(self):
        j = random.randint(self.n)
        e = slicesample(zeros(self.d), 1, self.K_e)
        s = self.datan[j,:] + self.h * self.lambdas[j] * e

        # Use mirroring technique to deal with boundary conditions.
        # Perhaps we should consider applying boundary kernels here...
        for k in xrange(self.d):
            if (s[k] < self.bounds[0,k]):
                s[k] = self.bounds[0,k]+abs(self.bounds[0,k]-s[k])
            if (s[k] > self.bounds[1,k]):
                s[k] = self.bounds[1,k]-abs(self.bounds[1,k]-s[k])
        return s

    # Estimate local bandwidth factors lambda(i)
    def setBandwithFactors(self, a):
        self.lambdas = ones(self.n)
        if (a > 0):
            B = [log10(f_pilot(self.datan[i,:], self.datan)) for i in xrange(self.n)] 
            g = pow(10,sum(B)/self.n)
            self.lambdas = [pow(f_pilot(self.datan[i,:], self.datan)/g,-a) for i in xrange(self.n)]

    # Epanechnikov kernel
    def K_e(self, t):
        return (self.d+2)/self.c_d*(1-dot(t,t))/2 if dot(t,t) < 1 else 0

    # Compute pilot density point estimate f(x)
    def f_pilot(self, x, datan):
        A = [K_e((x-datan[i,:])/self.h) for i in xrange(n)]
        return (pow(h,-d)*sum(A))/n

    # Computed here seperately to preserve readability of the equation. Otherwise nearly every 
    # variable is prefixed with "self."
    def compute_h(self, n, d, c_d, b):
        return b * pow( (8/c_d*(d+4) * pow(2*sqrt(pi),d) ), (1.0/(d+4))) * pow(n,-1.0/(d+4))


    # =============== Partitioned Sampling Methods =============== 
    def isGood(self, sample):
        return all(sample > self.inner[0,:]) and all(sample < self.inner[1,:])

    def isCritical(self, sample):
        return not (self.isGood(sample) or self.isFailing(sample))

    def isFailing(self, sample):
        return (any(sample < self.outer[0,:]) or any(sample > self.outer[1,:]))

