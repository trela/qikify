"""Implements MATLAB slice sampling."""

import numpy as np

def slicesample(x0, n_samples, pdf, width = 10, maxiter = 200):
    """Loosely based on slicesample() from MATLAB.
    """
    
    dim = np.size(x0)
    rnd = np.zeros((n_samples, dim))
    e   = np.random.exponential(1, n_samples) # for the vertical slice position.
    RW  = np.random.rand(n_samples, dim) # factors of randomizing the width
    RD  = np.random.rand(n_samples, dim) # uniformly draw point within the slice
    
    for i in xrange(n_samples):
        # A vertical level is drawn uniformly from (0,f(x0)) and used to define
        # the horizontal "slice".
        z = logpdf(x0, pdf) - e[i]
        
        # An interval [xl, xr] of width w is randomly position around x0 and
        # then expanded in steps of size w until both size are outside the
        # slice.
        r  = width * RW[i, :]
        xl = x0 - r 
        xr = xl + width 
        
        iteration = 0
        # step out procedure is performed only when univariate samples are
        # drawn.
        if dim == 1:
            # step out to the left.
            while inside(xl, z, pdf) and iteration < maxiter:
                xl -= width
                iteration += 1

            # step out to the right
            iteration = 0  
            while inside(xr, z, pdf) and iteration < maxiter:
                xr += width
                iteration += 1        

        # A new point is found by picking uniformly from the interval [xl, xr].
        xp = RD[i, :] * (xr - xl) + xl
    
        # shrink the interval (or hyper-rectangle) if a point outside the
        # density is drawn.
        iteration = 0
        while outside(xp, z, pdf) and iteration < maxiter:
            rshrink = (xp > x0)
            lshrink = ~rshrink
            xr[rshrink] = xp[rshrink]
            xl[lshrink] = xp[lshrink]
            xp = (np.random.rand(1, dim) * (xr - xl))[0] + xl # draw again
            iteration += 1
        rnd[i, :] = x0 = xp # update the current value 
    return (rnd[0, :] if n_samples == 1 else rnd)

def logpdf(xvar, pdf):
    """Returns the safe-log of the probability density function.
    """
    func_x = pdf(xvar)
    return np.log(func_x) if func_x > 0 else -np.inf

def inside(xvar, thresh, pdf):
    """Determines if logpdf sample is inside threshold.
    """
    return logpdf(xvar, pdf) > thresh

def outside(xvar, thresh, pdf):
    """Determines if logpdf sample is outside threshold.
    """
    return logpdf(xvar, pdf) <= thresh





