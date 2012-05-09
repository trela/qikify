"""Support Vector Machine implementation.
"""
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from qikify.helpers import standardize

class SVM(object):
    """Support Vector Machine implementation.
    """

    def __init__(self, grid_search = False):
        """Support Vector Machine implementation.
        
        Parameters
        ----------
        grid_search: boolean
                   Determine whether the SVM will perform a grid search to tune
                   hyperparameters.
        """
        self.model = None
        self.scale_dict = None
        self.grid_search = grid_search
        
        
    def fit(self, chips):
        """Train a support vector machine model.

        Parameters
        ----------
        chips: list
            Contains a stored array of Chip objects        
        """

        X   = [chip.LCT.values() for chip in chips]
        gnd = [chip.gnd for chip in chips]            
        
        if grid_search:
            grid = { 'C': [1, 5, 10, 50, 100], \
                 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1] }

            print 'SVM: Grid search using parameter grid: ', grid

            self.model = GridSearchCV(SVC(kernel='rbf'), grid, n_jobs=4, \
                            fit_params={'class_weight': {1 : 1, -1 : 1}})
        else:
            self.model = SVC()
            
        self.scale_factors, Xstd = standardize(X)
        self.model.fit(Xstd, gnd)


    def predict(self, chip):
        """Use the trained SVM model to predict.
        
        Parameters:
        ----------
        chip: chip model object
            Contains a chip's test data        
        """
        
        X = standardize(chip.LCT.values(), self.scale_factors)
        return self.model.predict(X)




