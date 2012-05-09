import ffx
from helpers import partition

class FFX(object):
    def __init__(self):
        pass
    
    def fit(self, chips):
        """Fit an FFX model.

        Parameters
        ----------
        chips : list
            A list of chip model objects.        
        """
        data = [chip.LCT.values() + [chip.gnd] for chip in chips]
        
        xtrain, ytrain, xtest, ytest = partition(data)
        
        self.models = ffx.run(self.xtrain, self.ytrain, self.xtest, self.ytest, self.data.columns)
        self.best_model = np.argmin([model.test_nmse for model in models])
        
    def predict(self, chip):
        """
        Parameters
        ----------
        chip: chip model object
            Contains a chip's test parameters 
        """        
        return self.models[self.best_model].simulate(chip.LCT.values())
        