"""Laplacian score feature selection.
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from qikify.helpers.helpers import standardize, zero_diag, set_submat, gen_max_mat
from qikify.helpers.term_helpers import Colors

# Laplacian score feature selection
class LSFS(object):
    """Laplacian score feature selection.
    """
    
    def __init__(self):
        self.col        = colors()
        self.ranking    = None
        self.scores     = None
        self.subset     = None
        self.n_retained = None
        
        
    def fit(self, chips):
        """Run Laplacian Score Feature Selection. 
         
        .. note:: Eventually, it'd be nice to maintain col names with Xin so
        that we can add a plot method to plot scores vs. column names.
        
        Notes
        -----
        This code is based on the definition from the paper [1]_:

        .. \\frac{\sum_{ij} (f_r^i - f_r^j) * S_{ij}}{sigma_2}

        .. [1] He, X. and Cai, D. and Niyogi, P., "Laplacian Score for Feature
        Selection", NIPS 2005.

        Parameters
        ----------
        chips : list
            A list of chip objects            
        """
        
        X   = np.array([chip.LCT.values() for chip in chips])
        gnd = np.array([chip.gnd for chip in chips])
        
        assert X.shape[0] == len(gnd), \
            "Data and gnd do not have matching sizes"
        
        _, X = standardize(X)
        
        # Per LSFS paper, S_ij = exp(-||x_i - x_j||^2 / t). I've found that
        # t = ncol(X) to be a suitable choice; anything on that order should 
        # work just fine.
        S          = self._construct_w(X, gnd, t=X.shape[1]) 
        D          = sum(S, 1)
        dot_d_x    = np.dot(D, X)
        z          = (dot_d_x * dot_d_x) / sum(D)  
        
        dprime = sum(np.dot(X.T, np.diag(D)).T * X, 0) - z      
        lprime = sum(np.dot(X.T, S).T * X, 1) - z
        
        
        # Remove trivial solutions
        dprime[dprime < 1e-12] = np.inf
        
        # Compute and retain Laplacian scores and rankings
        self.scores  = (lprime/dprime).T
        self.ranking = np.argsort(-self.scores)
        
        del S  # Clean up to save memory
        return self
        
    def threshold(self, thresh):
        """Threshold Laplacian scores, and return subset of features with 
        Laplacian scores above threshold."""
        self.subset    = self.scores > thresh
        self.n_retained = int(sum(self.subset))
        print 'LSFS: retained %s %d %s parameters.' % \
              (self.col.GREEN, self.n_retained, self.col.ENDC)
        return self.subset

    def _construct_w(self, 
                    X, 
                    gnd, 
                    t = 1, 
                    bLDA=False, 
                    self_connected=True):
        """Construct the w matrix used in LSFS.
        """
        label = np.unique(gnd)
        G     = np.zeros((len(gnd), len(gnd)))
        
        if bLDA:
            for i in xrange(len(label)):
                ind = (gnd==label[i])
                G[np.ix_(ind, ind)] = 1.0 / sum(ind)
            return G
            
        else:
            for i in xrange(len(label)):
                ind = np.nonzero(gnd==label[i])[0]

                # D_ij = ||x_i - x_j||^2
                D   = squareform(pdist(X[ind, :], 'sqeuclidean'))  
                
                # Per LSFS paper, exp(-||x_i - x_j||^2 / t)
                S   = np.exp(-D / t)                         
                
                set_submat(G, S, ind)                         
            if not self_connected:
                G = zero_diag(G)
            return gen_max_mat(G)
        print 'LSFS: Construction of W matrix complete.'


    def plot(self, filename):
        """Plot laplacian scores.
        """
        plt.plot(self.scores[self.ranking], 'k-')
        plt.grid(True)
        plt.xlabel('Features Retained')
        plt.ylabel('Laplacian Score')
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename, dpi=150, format='pdf')
        plt.close()


