"""Support Vector Machine implementation.
"""
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from qikify.helpers import standardize

class SVM(object):
    """Support Vector Machine implementation.
    """

    def __init__(self):
        self.model = None
        self.scale_dict = None
        
    def train(self, X, gnd, grid_search = False):
        """Train a support vector machine model.
        """
        if grid_search:
            grid = { 'C': [1, 5, 10, 50, 100], \
                 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1] }

            print 'SVM: Grid search using parameter grid: ', grid

            self.model = GridSearchCV(SVC(kernel='rbf'), grid, n_jobs=4, \
                            fit_params={'class_weight': {1 : 1, -1 : 1}})
        else:
            self.model = SVC()
        self.scale_dict = {'mean': X.mean(axis = 0), \
                            'std': X.std(axis = 0)}
        self.model.fit(standardize(X, self.scale_dict), gnd)

    def predict(self, X):
        """Use the trained SVM model to predict.
        """
        return self.model.predict(standardize(X, self.scale_dict))




