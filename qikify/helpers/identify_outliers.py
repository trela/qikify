"""Functions for identifying outliers.
"""

import numpy as np

def identify_outliers(data, k=3):
    """Compare a dataset against mean +/- k*sigma limits, and
    return a boolean vector with False elements denoting outliers.
    
    Parameters
    ----------
    data : Contains data stored in a pandas DataFrame or Series.
    """
    mean  = data.mean(0)
    sigma = data.std(0)
    lower, upper = mean-(k*sigma), mean+(k*sigma)
    
    # Change NaNs to +/- Inf
    lower[np.isnan(lower)] = -np.inf
    upper[np.isnan(upper)] = np.inf
    
    lsl   = np.tile(lower.tolist(), (data.shape[0], 1))
    usl   = np.tile(upper.tolist(), (data.shape[0], 1))
    pf_mat = np.logical_and(data >= lsl, data <= usl)
    return np.logical_and.reduce(pf_mat, 1)


def identify_outliers_specs(data, specs, k=3):
    """Compare a dataset against expanded spec limits, and
    return a boolean vector with False elements denoting outliers.
    
    Parameters
    ----------
    data : Contains data stored in a pandas DataFrame or Series.
    """
    pf_mat = np.ones(data.shape)
    mean   = data.mean(0)
    
    # Iterate over columns in pfData
    for j in xrange(pf_mat.shape[1]):
        lsl, usl = specs[data.columns[j]] if data.shape[1] > 1 \
                                          else specs[data.name]
        lsl = mean[j] - k * abs(mean[j] - lsl) if not np.isnan(lsl) else np.nan
        usl = mean[j] + k * abs(mean[j] - usl) if not np.isnan(usl) else np.nan
        
        pf_mat[:, j] = data.ix[:, j].apply(lambda x: x >= lsl and x <= usl)

    return (np.sum(pf_mat, 1) == data.shape[1])



