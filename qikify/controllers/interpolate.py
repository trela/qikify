import numpy as np

def lerp(x, xlim, ylim):
    """linearly interpolate a value of y given ranges for x, y.
    
    arguments:
        x: scalar
        xlim: array with xmin, xmax
        ylim: array with ymin, ymax
    """
    dx = (x - xlim[0])
    m = ((ylim[1] - ylim[0]) / (xlim[1] - xlim[0]))
    y = ylim[0] + m * dx
    return y
    

def bilinear_interp(x, y, xlim, ylim, Q):
    """bilinear interpolation of z over 2d surface {x,y}"""
    denom = (xlim[1] - xlim[0])*(ylim[1] - ylim[0])
    
    return Q[0,0] / denom * (xlim[1] - x) * (ylim[1] - y) + \
           Q[1,0] / denom * (x - xlim[0]) * (ylim[1] - y) + \
           Q[0,1] / denom * (xlim[1] - x) * (y - ylim[0]) + \
           Q[1,1] / denom * (x - xlim[0]) * (y - ylim[0])

    

def cart2polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.degrees(np.arctan2(y, x))
    if np.isscalar(theta) and (theta < 0):
        theta += 360
    if theta.size > 1:
        theta[theta < 0] += 360
    return r, theta

def polar2cart(r, theta):
    theta = np.deg2rad(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y
   
def cart2polar_recenter(x, y, xmax, ymax):
    xm, ym = x - ((xmax+1) / 2.0), y - ((ymax+1) / 2.0)
    r, theta = cart2polar(xm, ym)
    return r, theta

def polar2cart_recenter(r, theta, xmax, ymax):
    x, y = polar2cart(r, theta)
    return x+((xmax+1) / 2.0), y+((ymax+1) / 2.0)
    
    
    