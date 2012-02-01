import numpy as np
from scipy.stats.stats import kurtosis
from scipy import c_,r_

from qikify.controllers.identifyOutliers import *
import qikify.controllers.FFX as FFX
from qikify.controllers.KDE import KDE
from qikify.controllers.LSFS import LSFS
from qikify.models.Specs import Specs
from qikify.models.dotdict import dotdict
import pandas


def test_identifyOutliers():
    """Test for the identifyOutliers controller. 
    TODO: At the moment, this only tests the mu +/- k sigma outlier filter, 
    not the spec-based outlier filter.
    """
    A       = pandas.DataFrame(np.ones((100,3)))
    A.ix[99,2] = 30
    assert identifyOutliers(A, 6).tolist() == [True]*99 + [False]
    
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
    X   = pandas.DataFrame(np.random.multivariate_normal([0,0], np.eye(2), (1000,)))
    S   = kde.run(X, nSamples = 1000)
    assert np.mean( S.std(0) - X.std(0))    < eps
    assert np.mean( S.mean(0) - X.mean(0))  < eps
    assert np.mean(kurtosis(S,0) - kurtosis(X, 0)) < eps

    # Test partitioned KDE
    counts = dotdict({'nGood': 250, 'nCritical': 100, 'nFail': 100})
    columns  = ['A', 'B']
    specLims = pandas.DataFrame({columns[0]: np.array([-2.0,2.0]), columns[1]: np.array([-2.0,2.0])})
    specs  = Specs(specs=specLims).genCriticalRegion(5.5/6, 6.5/6)
    A   = pandas.DataFrame(np.random.multivariate_normal([0,0], np.eye(2), (1000,)), columns=columns)
    S   = kde.run(A,specs=specs,counts=counts)
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
    Xa = (np.random.randn(500,2) / 10) + [1,1]
    Xb = (np.random.randn(500,2) / 10) + [-1,-1]
    y = r_[np.ones((500,)), np.zeros((500,))]
    X = c_[r_[Xa, Xb], np.random.randn(1000,10)]
    lsfs.run(X,y)
    assert abs(sum(lsfs.Scores[0:2]) - 2.0) < 0.2
    assert np.mean(lsfs.Scores[2:]) < 0.25




class TestFFX:
    def setUp(self): 
        self.EPS = 0.001
        self.data = pandas.read_csv('iris.csv')
        self.xtrain_pandas = self.data.ix[:50,0:2]
        self.xtest_pandas  = self.data.ix[51:100,0:2]
        self.xtrain        = self.xtrain_pandas.as_matrix()
        self.ytrain        = self.data.ix[:50,2]
        self.xtest         = self.xtest_pandas.as_matrix()
        self.ytest  = self.data.ix[51:100,2]

    def similar(self, a, b):
        return sum(abs(a - b)) < self.EPS

    # ----------------------------------------------------------------
    # Test bases
    # ----------------------------------------------------------------
    def runBase(self, model, data):
        return self.similar(model.simulate(self.xtrain), data)

    def testSimpleBase(self):
        assert self.runBase(FFX.SimpleBase(0,1), self.xtrain[:,0])
        assert self.runBase(FFX.SimpleBase(0,2), self.xtrain[:,0]**2)

    def testOperatorBase(self):
        a = FFX.SimpleBase(0,1)
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_ABS),        np.abs(self.xtrain[:,0]))
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_MAX0),       np.clip(self.xtrain[:,0], 0.0, FFX.INF))
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_MIN0),       np.clip(self.xtrain[:,0], -FFX.INF, 0.0))
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_LOG10),      np.log10(self.xtrain[:,0]))
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_GTH, 0.5),   np.clip(0.5 - self.xtrain[:,0], 0.0, FFX.INF))
        assert self.runBase(FFX.OperatorBase(a, FFX.OP_LTH, 0.5),   np.clip(self.xtrain[:,0] - 0.5, 0.0, FFX.INF))

    def testProductBase(self):
        a = FFX.SimpleBase(0,1)
        b = FFX.SimpleBase(0,1)
        c = FFX.SimpleBase(0,2)
        assert self.runBase(FFX.ProductBase(a,b), self.xtrain[:,0]**2)
        assert self.runBase(FFX.ProductBase(a,c), self.xtrain[:,0]**3)


    # ----------------------------------------------------------------
    # Test models
    # ----------------------------------------------------------------
    def testConstantModel(self):
        mu = self.xtrain[:,0].mean()
        a  = FFX.ConstantModel(mu,0).simulate(self.xtrain)
        assert self.runBase(FFX.ConstantModel(mu,0),np.repeat(mu, self.xtrain.shape[0]))

    def testMultiFFXModelFactory(self):
        # Use numpy.ndarray
        models = FFX.MultiFFXModelFactory().build(self.xtrain, self.ytrain, self.xtest, self.ytest, self.data.columns)
        assert abs(np.mean([model.test_nmse for model in models]) - 0.4391323) < self.EPS

        # Use pandas.DataFrame
        models = FFX.MultiFFXModelFactory().build(self.xtrain_pandas, self.ytrain, self.xtest_pandas, self.ytest)
        assert abs(np.mean([model.test_nmse for model in models]) - 0.4391323) < self.EPS        




