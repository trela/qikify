"""Functions for numerical interpolation.
"""

import numpy as np

def lerp(xvar, xlim, ylim):
    """linearly interpolate a value of y given ranges for x, y.
    
    arguments:
        xvar: scalar
        xlim: array with xmin, xmax
        ylim: array with ymin, ymax
    """
    delta_x = (xvar - xlim[0])
    slope = ((ylim[1] - ylim[0]) / (xlim[1] - xlim[0]))
    yvar = ylim[0] + slope * delta_x
    return yvar
    

def bilinear_interp(xvar, yvar, xlim, ylim, zvar):
    """bilinear interpolation of z over 2d surface {x,y}"""
    denom = (xlim[1] - xlim[0]) * (ylim[1] - ylim[0])
    
    return zvar[0, 0] / denom * (xlim[1] - xvar) * (ylim[1] - yvar) + \
           zvar[1, 0] / denom * (xvar - xlim[0]) * (ylim[1] - yvar) + \
           zvar[0, 1] / denom * (xlim[1] - xvar) * (yvar - ylim[0]) + \
           zvar[1, 1] / denom * (xvar - xlim[0]) * (yvar - ylim[0])


def cart2polar(xvar, yvar):
    """Convert Cartesian coordinates to polar.
    """
    rad   = np.sqrt(xvar**2 + yvar**2)
    theta = np.degrees(np.arctan2(yvar, xvar))
    if np.isscalar(theta) and (theta < 0):
        theta += 360
    if theta.size > 1:
        theta[theta < 0] += 360
    return rad, theta

def polar2cart(rad, theta):
    """Convert polar coordinates to Cartesian.
    """
    theta = np.deg2rad(theta)
    xvar = rad * np.cos(theta)
    yvar = rad * np.sin(theta)
    return xvar, yvar
   
   
def cart2polar_recenter(xvar, yvar, xmax, ymax):
    """Convert Cartesian coordinates to polar, with recentering.
    """
    xmax_c, ymax_c = xvar - ((xmax+1) / 2.0), yvar - ((ymax+1) / 2.0)
    return cart2polar(xmax_c, ymax_c)


def polar2cart_recenter(rad, theta, xmax, ymax):
    """Convert polar coordinates to Cartesian with recentering.
    """    
    xvar, yvar = polar2cart(rad, theta)
    return xvar+((xmax+1) / 2.0), yvar+((ymax+1) / 2.0)
    
    
    
    
    