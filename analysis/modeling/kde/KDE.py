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

sys.path.append( os.path.join( os.getcwd(), '..'))
from ..helpers.general import *
from slicesample import * 

class KDE:
	def __init__(self, data, bounds = None):
		
		self.n = size(data, 0)
		self.d = size(data,1)
		self.b = 0.8			# Default bandwidth scaling factor
		
		# Normalize data
		self.scaleDict 	= dotdict({'mean': data.mean(axis = 0), 'std': data.std(axis = 0)})
		self.datan 		= scale(data, self.scaleDict)
		if bounds is None:
			self.bounds 	= scale(array([data.min(axis=0), data.max(axis=0)]), self.scaleDict)
		else:
			self.bounds 	= scale(array(bounds), self.scaleDict)
			
		# Select bandwidth for Epanechnikov kernel (Rule of Thumb, see Silverman, p.86)
		self.c_d = 2.0* pow( pi, (self.d/2.0) ) / ( self.d * gamma(self.d/2) )
		self.h   = self.compute_h(self.n, self.d, self.c_d, self.b)


	def run(self, numSamples, a = 0):
		# Estimate local bandwidth factors lambda(i)
		lambdaFactors = ones(self.n)
		if (a > 0):
			B = [log10(f_pilot(self.datan[i,:], self.datan)) for i in range(self.n)] 
			g = pow(10,sum(B)/self.n)
			lambdaFactors = [pow(f_pilot(self.datan[i,:], self.datan)/g,-a) for i in range(self.n)]

		# Use algorithm in Silverman, p. 143
		Sn = zeros((numSamples, self.d))
		for i in range(numSamples):
			j = random.randint(self.n)
			e = slicesample(zeros(self.d), 1, self.K_e)
			s = self.datan[j,:] + self.h * lambdaFactors[j] * e
			
			for k in range(self.d):
				if (s[k] < self.bounds[0,k]):
					s[k] = self.bounds[0,k]+abs(self.bounds[0,k]-s[k])
				if (s[k] > self.bounds[1,k]):
					s[k] = self.bounds[1,k]-abs(self.bounds[1,k]-s[k])
			Sn[i,:] = s
		return scale(Sn, self.scaleDict, reverse = True);

	# Epanechnikov kernel
	def K_e(self, t):
		return (self.d+2)/self.c_d*(1-dot(t,t))/2 if dot(t,t) < 1 else 0

	# Compute pilot density point estimate f(x)
	def f_pilot(self, x, datan):
		A = [K_e((x-datan[i,:])/h) for i in range(n)]
		return (pow(h,-d)*sum(A))/n

	# Computed here seperately to preserve readability of the equation. Otherwise nearly every 
	# variable is prefixed with "self."
	def compute_h(self, n, d, c_d, b):
		return b * pow( (8/c_d*(d+4) * pow(2*sqrt(pi),d) ), (1.0/(d+4))) * pow(n,-1.0/(d+4))
		
		
	


