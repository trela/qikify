import numpy as np
import pandas
from scipy.spatial.distance import pdist, squareform
from qikify.helpers import standardize

# Laplacian score feature selection
class LSFS(object):
    def run(self, Xin, gnd):
        """Run Laplacian Score Feature Selection. 
         
        .. note:: Eventually, it'd be nice to maintain col names with Xin so that we can add a plot method to plot scores vs. column names.
        
        Notes
        -----
        This code is based on the definition from the paper [1]_:

        .. \\frac{\sum_{ij} (f_r^i - f_r^j) * S_{ij}}{sigma_2}

        .. [1] He, X. and Cai, D. and Niyogi, P., "Laplacian Score for Feature Selection", NIPS 2005.

        Parameters
        ----------
        Xin : array_like
            A numpy.ndarray or pandas.DataFrame, with rows corresponding to observations and columns to features.
            
        gnd : array_like
            A numpy.ndarray or pandas.DataFrame pass/fail vector of the same dimension as Xin
        
        
        """
        if isinstance(Xin, pandas.DataFrame):
            X = Xin.as_matrix()
        else:
            X = Xin
        
        nSmp = X.shape[0]
        if nSmp != len(gnd): 
            raise Exception("Data and gnd do not have matching sizes")
        
        _, X = standardize(X)
        
        # Per LSFS paper, S_ij = exp(-||x_i - x_j||^2 / t). I've found that
        # t = ncol(X) to be a suitable choice; anything on that order should 
        # work just fine.
        S          = self.constructS(X, gnd, t=X.shape[1]) 
        D          = sum(S,1)
        z          = (np.dot(D,X) * np.dot(D,X)) / sum(D)  
        
        DPrime     = sum(np.dot(X.T,np.diag(D)).T * X,0) - z      
        LPrime     = sum((np.dot(X.T,S).T * X),1) - z
        
        
        # Remove trivial solutions
        DPrime[DPrime < 1e-12] = np.inf
        
        # Compute and retain Laplacian scores and rankings
        self.Scores    = (LPrime/DPrime).T
        self.Ranking   = np.argsort(-self.Scores)
        
        del S  # Clean up to save memory
        return self
        
    def threshold(self, T_L):
        self.subset    = self.Scores > T_L
        self.nRetained = int(sum(self.subset))
        print 'LSFS: retained', GREEN+str(self.nRetained)+ENDCOLOR, 'parameters.'
        return self.subset

    # Construct the W matrix used in LSFS
    def constructS(self, X, gnd, k = 0, t = 1, bLDA=False, bSelfConnected=True):
        label = np.unique(gnd)
        G     = np.zeros((len(gnd),len(gnd)))
        if bLDA:
            for i in xrange(len(label)):
                ind = (gnd==label[i])
                G[ix_(ind,ind)] = 1.0/sum(ind)
            return G
        else:
            for i in xrange(len(label)):
                ind = np.nonzero(gnd==label[i])[0]
                D   = squareform(pdist(X[ind,:], 'sqeuclidean'))  # D_ij = ||x_i - x_j||^2
                S   = np.exp(-D/t)                                   # Per LSFS paper, exp(-||x_i - x_j||^2 / t)
                self._setSubMat(G, S, ind)                         
            if not bSelfConnected:
                G = zeroMatrixDiagonal(G)
            return self._genMaxMatrix(G)
        print 'LSFS: Construction of W matrix complete.'

    def _setSubMat(self, X, D, ind):
        """Set a submatrix of X defined by the index ind to values in D. 
        That is:
                 [0, 0, 0]
             X = [0, 0, 0]   D = [1 2] ind = [0 1]
                 [0, 0, 0]       [3 4]
        Gives:
                 [1, 2, 0]
             X = [3, 4, 0]
                 [0, 0, 0]
        """
        for i, row in enumerate(ind):
            X[row,ind] = D[i,:]

    def _genMaxMatrix(self, A):
        """Takes a square matrix A and computes max(A, A')"""
        ind = (A.T - A) > 0
        A[ind] = A.T[ind]
        return A

