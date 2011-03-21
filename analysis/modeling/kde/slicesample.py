#!/usr/bin/python
'''

Loosely based on slicesample() from MATLAB.
 
'''

from numpy import *


def slicesample(initial, nsamples, pdf, width = 10, maxiter = 200):
	dim = size(initial)
	rnd = zeros((nsamples,dim))

	e   = random.exponential(1,nsamples) # needed for the vertical position of the slice.
	RW  = random.rand(nsamples,dim) # factors of randomizing the width
	RD  = random.rand(nsamples,dim) # uniformly draw the point within the slice
	x0  = initial
	
	for i in range(nsamples):
		# A vertical level is drawn uniformly from (0,f(x0)) and used to define
		# the horizontal "slice".
		z = logpdf(x0, pdf) - e[i]
		
		# An interval [xl, xr] of width w is randomly position around x0 and then
		# expanded in steps of size w until both size are outside the slice.   
		r  = width * RW[i,:]
		xl = x0 - r 
		xr = xl + width 
		
		iteration = 0
	    # step out procedure is performed only when univariate samples are drawn.
		if dim==1:
			# step out to the left.
			while inside(xl,z, pdf) and iteration < maxiter:
				xl -= width
				iteration += 1

			# step out to the right
			iteration = 0  
			while inside(xr,z, pdf) and iteration < maxiter:
				xr += width
				iteration += 1        

	    # A new point is found by picking uniformly from the interval [xl, xr].
		xp = RD[i,:]*(xr-xl) + xl
		
	    # shrink the interval (or hyper-rectangle) if a point outside the
	    # density is drawn.
		iteration = 0
		while outside(xp,z, pdf) and iteration < maxiter:
			rshrink = (xp > x0)
			xr[rshrink] = xp[rshrink]
			lshrink = ~rshrink
			xl[lshrink] = xp[lshrink]
			xp = (random.rand(1,dim) * (xr-xl))[0] + xl # draw again
			iteration += 1
			
		x0 = xp # update the current value 
		rnd[i,:] = x0
		
	return (rnd[0,:] if nsamples == 1 else rnd)


def logpdf(x, pdf):
	fx 		= pdf(x)
	return log(fx) if fx > 0 else -inf

def inside(x,th, pdf):
	return logpdf(x, pdf) > th

def outside(x,th, pdf):
	return ~inside(x,th, pdf)


