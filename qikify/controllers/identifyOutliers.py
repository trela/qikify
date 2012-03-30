import numpy as np

def identifyOutliers(data, k=3):
    """Compare a dataset against mu +/- k*sigma limits, and
    return a boolean vector with False elements denoting outliers.
    
    Parameters
    ----------
    data : Contains data stored in a pandas DataFrame or Series.
    """
    mu    = data.mean(0)
    sigma = data.std(0)
    lower, upper = mu-(k*sigma), mu+(k*sigma)
    
    # Change NaNs to +/- Inf
    lower[np.isnan(lower)] = -np.inf
    upper[np.isnan(upper)] = np.inf
    
    lsl   = np.tile(lower.tolist(), (data.shape[0], 1))
    usl   = np.tile(upper.tolist(), (data.shape[0], 1))
    pfMat = np.logical_and(data >= lsl, data <= usl)
    return np.logical_and.reduce(pfMat,1)


def identifyOutliersSpecs(data, specs, ind, k=3):
    """Compare a dataset against expanded spec limits, and
    return a boolean vector with False elements denoting outliers.
    
    Parameters
    ----------
    data : Contains data stored in a pandas DataFrame or Series.
    """
    pfMat = np.ones(data.shape)
    mu    = data.mean(0)
    
    # Iterate over columns in pfData
    for j in xrange(pfData.shape[1]):
        lsl, usl = specs[data.columns[j]] if data.shape[1] > 1 else specs[data.name]
        lsl = mu[j] - k * abs(mu[j] - lsl) if not np.isnan(lsl) else np.nan
        usl = mu[j] + k * abs(mu[j] - usl) if not np.isnan(usl) else np.nan
        pfMat[:,j]  = data.ix[:,j].apply(lambda x: x >= lsl and x <= usl)
    return (np.sum(pfMat, 1) == data.shape[1])



