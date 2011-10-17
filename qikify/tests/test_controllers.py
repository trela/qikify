import numpy as np
from scipy.stats.stats import kurtosis

from qikify.controllers.identifyOutliers import *
from qikify.controllers.KDE import KDE
from qikify.models.DataStruct import DataStruct
from qikify.models.Specs import Specs
from qikify.models.dotdict import dotdict

def test_identifyOutliers():
    A       = DataStruct(np.ones((100,3)))
    A[99,2] = 30
    assert identifyOutliers(A, 6).tolist() == [True]*99 + [False]
    
def test_kde():
    eps = 0.1
    kde = KDE()
    A   = np.random.multivariate_normal([0,0], np.eye(2), (1000,))
    S   = kde.run(A, nSamples = 1000)
    assert np.mean(  np.std(S,0) - np.std(A,0))    < eps
    assert np.mean( np.mean(S,0) - np.mean(A,0))   < eps
    assert np.mean(kurtosis(S,0) - kurtosis(A, 0)) < eps
    
def test_partitioned_kde():
    kde    = KDE()
    counts = dotdict({'nGood': 5000, 'nCritical': 2000, 'nFail': 2000})
    eps    = 0.1
    names  = ['A', 'B']
    specs  = Specs(names=names, specs={'A': np.array([-2,2]), 'B': np.array([-2,2])}).genCriticalRegion(5.5/6, 6.5/6)
    A   = DataStruct(np.random.multivariate_normal([0,0], np.eye(2), (10000,)), names=names)
    S   = kde.run(A,specs=specs,counts=counts)
    assert np.mean(  np.std(S,0) - 1.3 * np.std(A,0)) < eps
    assert np.mean( np.mean(S,0) - np.mean(A,0))      < eps

