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
from numpy import *
from scipy.special import gamma

from helpers.general import *
from models.Specs import Specs
from slicesample import * 

class KDE:

	# Primary execution point. Run either standard KDE or class-membership based KDE. If 
	# any of the class-membership based KDE arguments are set, it will be run instead of 
	# standard KDE.
	def run(self, data, a = 0, specs = None, bounds = None, nSamples = 0, nGood = 0, nCritical = 0, nFail = 0, inner = None, outer = None):
		self.n 	 = size(data,0)
		self.d 	 = size(data,1)
		self.b 	 = 0.8			# Default bandwidth scaling factor

		# Select bandwidth for Epanechnikov kernel (Rule of Thumb, see Silverman, p.86)
		self.c_d = 2.0* pow( pi, (self.d/2.0) ) / ( self.d * gamma(self.d/2) )
		self.h   = self.compute_h(self.n, self.d, self.c_d, self.b)
		self.setBandwithFactors(a)

		# Normalize data
		self.scaleFactors 	= dotdict({'mean': data.mean(axis = 0), 'std': data.std(axis = 0)})
		self.datan 			= scale(data, self.scaleFactors)
		if bounds is None:
			self.bounds 	= scale(array([data.min(axis=0), data.max(axis=0)]), self.scaleFactors)
		else:
			self.bounds 	= scale(bounds, self.scaleFactors)

		if specs is not None:
			self.specs = specs

		
		# Generate nGood, nCritical, nFail samples.
		if sum((nGood, nCritical, nFail)) > 0:
			self.inner = inner
			self.outer = outer
			return self.genPartitionedSamples(nGood, nCritical, nFail)
			
		# Otherwise, just generate nSamples without caring about device good/critical/bad membership.
		else:
			return self.genSamples(nSamples)




	# =============== Private class methods =============== 
	# Default method of generating device samples
	def genSamples(self, nSamples):
		Sn = vstack([ self.genSample() for _ in xrange(nSamples) ])
		return scale(Sn, self.scaleFactors, reverse = True)
		
	# Generates Ngc critical devices, Ng good devices, Nf failing devices.
	def genPartitionedSamples(self, nGood, nCritical, nFail):
		# Initialize arrays for speed
		Sg, Sc, Sf = zeros((nGood, self.d)), zeros((nCritical, self.d)), zeros((nFail, self.d))
		
		ng = nc = nf = 0
		
		import pdb; pdb.set_trace()
		
		while (ng+nc+nf < nGood + nCritical + nFail):
			sample = scale(self.genSample(), self.scaleFactors, reverse = True)
			if self.isGood(sample) and ng < nGood:
				ng += 1
				Sg[ng,:] = sample
			if self.isFailing(sample) and nf < nFail:
				nf += 1
				Sf[nf,:] = sample
			if self.isCritical(sample) and nc < nCritical:
				nc += 1
				Sc[nc,:] = sample
		
		return vstack((Sgc,Sg,Sf))


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
		A = [K_e((x-datan[i,:])/h) for i in xrange(n)]
		return (pow(h,-d)*sum(A))/n

	# Computed here seperately to preserve readability of the equation. Otherwise nearly every 
	# variable is prefixed with "self."
	def compute_h(self, n, d, c_d, b):
		return b * pow( (8/c_d*(d+4) * pow(2*sqrt(pi),d) ), (1.0/(d+4))) * pow(n,-1.0/(d+4))
	

	# =============== Partitioned Sampling Methods =============== 
	def isGood(self, sample):
		for val, [lsl,usl] in zip(sample[10:], self.inner.tolist()):
			if self.specs.compareToSpecs(val,lsl,usl) == -1:
				return False
		return True

	def isCritical(self, sample):
		return ~((self.isGood(sample) == 1) or (self.isFailing(sample) == 1))

	def isFailing(self, sample):
		for val, [lsl,usl] in zip(sample[10:], self.outer.tolist()):
			if self.specs.compareToSpecs(val,lsl,usl) == -1:
				return True
		return False
