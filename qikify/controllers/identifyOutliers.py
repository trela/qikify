import numpy as np

# Identify outliers using boundaries with margins determined by k.
def identifyOutliers(data, k=3):
    mu    = np.mean(data,0)
    sigma = np.std(data,0)
    lsl   = np.tile(mu-(k*sigma), (data.nrow, 1))
    usl   = np.tile(mu+(k*sigma), (data.nrow, 1))
    pfMat = np.logical_and(data >= lsl, data <= usl)
    return np.logical_and.reduce(pfMat,1)


'''
def identifyOutliersSpecs(self, specs, ind, k=3):
    pfMat = np.ones(self.shape)
    mu    = np.mean(self,0)

    # Iterate over columns in pfData     
    for j in xrange(self.ncol):
        lsl, usl = specs[self.names[j]] if self.ncol > 1 else specs[self.names]
        if k is not None:
            lsl = mu[j] - k_l * abs(mu[j] - lsl) if not np.isnan(lsl) else np.nan
            usl = mu[j] + k_u * abs(mu[j] - usl) if not np.isnan(usl) else np.nan
        pfMat[:,j]  = specs.compare(self[:,j], lsl, usl)
    return (np.sum(pfMat, 1) == self.ncol)
'''