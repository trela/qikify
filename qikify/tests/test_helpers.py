from qikify.helpers.helpers import computeR2
import numpy as np

def test_stats():
    eps = 0.01
    
    # Anscombe's Quartet #1
    x = np.array([10.0, 8.0, 13.0, 9.0, 11.0, 14.0, \
                   6.0, 4.0, 12.0, 7.0, 5.0])
    y = np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, \
                  7.24, 4.26, 10.84, 4.82, 5.68])
                  
    assert (computeR2(x, y) - 0.666542459) < eps

