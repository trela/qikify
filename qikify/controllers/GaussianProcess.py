import numpy as np
from sklearn.gaussian_process import GaussianProcess


class GaussianProcess(object):
    def __init__(self, nugget=0.1):
        self.nugget = nugget
        
    def fit(self, chips):
        X = pandas.DataFrame([[chip.X, chip.Y] for chip in chips])
        y = [chip.gnd for chip in chips]        
        self.gp = GaussianProcess(nugget=self.nugget)
        self.gp.fit(X, y)
    
    def predict(self, chip):
        return self.gp.predict([chip.X, chip.Y])
    