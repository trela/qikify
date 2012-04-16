import pandas
import numpy as np
from scipy.stats.stats import kurtosis
from scipy import c_, r_

from qikify.helpers.identify_outliers import identify_outliers

from qikify.controllers.KNN import KNN
from qikify.controllers.KDE import KDE
from qikify.controllers.LSFS import LSFS
from qikify.models.chip import Chip
from qikify.models.specs import Specs


def test_identify_outliers():
    """Test for the identifyOutliers controller. 
    TODO: At the moment, this only tests the mu +/- k sigma outlier filter, 
    not the spec-based outlier filter.
    """
    A       = pandas.DataFrame(np.ones((100, 3)))
    A.ix[99, 2] = 30
    assert identify_outliers(A, 6).tolist() == [True] * 99 + [False]
    
def test_kde():
    """
    Tests for kernel density estimation. To test standard KDE, we use a random
    normal to learn the density, generate 1000 samples, and then check that the
    means/standard deviations/kurtosis figures are similar to within a margin 
    epsilon.
    TODO: Need a test that adjusts the bandwidth factor a.
    """
    eps = 0.1
    kde = KDE()
    
    # Test standard KDE.
    X   = pandas.DataFrame(np.random.multivariate_normal([0, 0], \
                           np.eye(2), (1000, )))
    S   = kde.run(X, n_samples = 1000)
    assert np.mean( S.std(0) - X.std(0))    < eps
    assert np.mean( S.mean(0) - X.mean(0))  < eps
    assert np.mean(kurtosis(S, 0) - kurtosis(X, 0)) < eps

    # Test partitioned KDE
    counts   = {'nGood': 250, 'nCritical': 100, 'nFail': 100}
    columns  = ['A', 'B']
    spec_lims = pandas.DataFrame({columns[0]: np.array([-2.0, 2.0]), \
                                  columns[1]: np.array([-2.0, 2.0])})
    specs  = Specs(specs=spec_lims).gen_crit_region(5.5/6, 6.5/6)
    A   = pandas.DataFrame(np.random.multivariate_normal([0, 0], \
                           np.eye(2), (1000, )), columns=columns)
    S   = kde.run(A, specs=specs, counts=counts)
    assert np.mean(  S.std(0) - 1.3 * A.std(0)) < eps
    assert np.mean( S.mean(0) - A.mean(0))      < eps


def test_lsfs():
    """Tests for Laplacian score feature selection. We create a matrix where 
    the first two columns are very good discriminators of the class label, and 
    all the remaining features are random. Then run LSFS and ensure the scores 
    for the first two features are close to 1.0, and the remaining scores are
    small (less than 0.25).
    """
    lsfs = LSFS()
    Xa = (np.random.randn(500, 2) / 10) + [1, 1]
    Xb = (np.random.randn(500, 2) / 10) + [-1, -1]
    y = r_[np.ones((500, )), np.zeros((500, ))]
    X = c_[r_[Xa, Xb], np.random.randn(1000, 10)]
    lsfs.run(X, y)
    assert abs(sum(lsfs.scores[0:2]) - 2.0) < 0.2
    assert np.mean(lsfs.scores[2:]) < 0.25



def test_knn():
    knn = KNN(n_neighbors=1)
    chip_data1 = {'ORB_a':1, 'ORB_b':1, 'gnd':1}
    chip_data2 = {'ORB_a':-1, 'ORB_b':-1, 'gnd':-1}
    chip1 = Chip(chip_data1, LCT_prefix='ORB')
    chip2 = Chip(chip_data2, LCT_prefix='ORB')
    chips = [chip1, chip2]

    knn.fit(chips)

    chip3 = Chip({'ORB_a':0.9, 'ORB_b':0.9, 'gnd':1}, LCT_prefix='ORB')
    assert knn.predict(chip3) == 1, 'fail: prediction not correct.'



