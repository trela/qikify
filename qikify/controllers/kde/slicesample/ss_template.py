def slicesample(x0, pdf, width = 10, maxiter = 200):
    n = size(x0)
    rnd = zeros(n)
    e   = random.exponential(1) # needed for the vertical position of the slice.
    RW  = random.rand(n) # factors of randomizing the width
    RD  = random.rand(n) # uniformly draw the point within the slice

    z = logpdf(x0, pdf) - e
    r  = width * RW
    xl = x0 - r 
    xr = xl + width 
    
    iteration = 0
    
    if n==1:
        while inside(xl,z, pdf) and iteration < maxiter:
            xl -= width
            iteration += 1

        iteration = 0  
        while inside(xr,z, pdf) and iteration < maxiter:
            xr += width
            iteration += 1        

    xp = RD*(xr-xl) + xl

    iteration = 0
    while outside(xp,z, pdf) and iteration < maxiter:
        rshrink = (xp > x0)
        lshrink = ~rshrink
        xr[rshrink] = xp[rshrink]
        xl[lshrink] = xp[lshrink]
        xp = (random.rand(1,n) * (xr-xl))[0] + xl # draw again
        iteration += 1
    rnd = x0 = xp # update the current value 
    return rnd

def logpdf(x, pdf):
    fx = pdf(x)
    return log(fx) if fx > 0 else -inf

def inside(x,th, pdf):
    return logpdf(x, pdf) > th

def outside(x,th, pdf):
    return logpdf(x, pdf) <= th


