import numpy as np
from scipy.stats.stats import kurtosis

from qikify.controllers.identifyOutliers import *
from qikify.controllers.KDE import KDE
from qikify.models.Specs import Specs
from qikify.models.dotdict import dotdict
import pandas


def test_identifyOutliers():
    A       = pandas.DataFrame(np.ones((100,3)))
    A.ix[99,2] = 30
    assert identifyOutliers(A, 6).tolist() == [True]*99 + [False]
    
def test_kde():
    eps = 0.1
    kde = KDE()
    X   = pandas.DataFrame(np.random.multivariate_normal([0,0], np.eye(2), (1000,)))
    S   = kde.run(X, nSamples = 1000)
    assert np.mean( S.std(0) - X.std(0))    < eps
    assert np.mean( S.mean(0) - X.mean(0))  < eps
    assert np.mean(kurtosis(S,0) - kurtosis(X, 0)) < eps

def test_partitioned_kde():
    kde    = KDE()
    counts = dotdict({'nGood': 2500, 'nCritical': 1000, 'nFail': 1000})
    eps    = 0.1
    names  = ['A', 'B']
    specs  = Specs(names=names, specs={'A': np.array([-2,2]), 'B': np.array([-2,2])}).genCriticalRegion(5.5/6, 6.5/6)
    
    A   = pandas.DataFrame(np.random.multivariate_normal([0,0], np.eye(2), (10000,)), columns=names)
    S   = kde.run(A,specs=specs,counts=counts)
    assert np.mean(  S.std(0) - 1.3 * A.std(0)) < eps
    assert np.mean( S.mean(0) - A.mean(0))      < eps
