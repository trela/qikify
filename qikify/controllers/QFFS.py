"""Qikify feature selection.
"""

import numpy as np
from qikify.helpers import compute_corr_coefs

class QFFS(object):
    """Qikify feature selection library. Doesn't do much yet; right now only
    implements correlation coefficient-based feature selection. 
    """
    
    def __init__(self):
        pass
        
    def fit(self, X, y, n_features=10, intercept=True, method='corrcoef'):
        """Do feature selection on the basis of correlation coefficients.
        
        Parameters
        ----------
        X : numpy array of shape [n_samples,n_features]
            Training data

        y : numpy array of shape [n_samples]
            Target values

        n_features : int, optional
            Number of features to retain

        intercept : bool, optional
            Whether the first column is an all-constant intercept and 
            should be excluded

        method : string, optional
            Determines the feature selection method to use.

        Returns
        -------
        features : The X column indices to retain.

        Notes
        -----
        We typically exclude the first column since it is the intercept
        all-constant column.
        """
        
        if method == 'corrcoef':
            if intercept:
                _, cc_sorted = compute_corr_coefs(X[:, 1:], y)
                return np.concatenate(([0], cc_sorted[0:n_features] + 1))
            else:
                _, cc_sorted = compute_corr_coefs(X, y)
                return cc_sorted[0:n_features]




