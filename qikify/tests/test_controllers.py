import numpy as np
from qikify.controllers.identifyOutliers import *
from qikify.models.DataStruct import DataStruct

def test_identifyOutliers():
    A       = DataStruct(np.ones((100,3)))
    A[99,2] = 30
    assert identifyOutliers(A, 6).tolist() == [True]*99 + [False]
    