import numpy as np

from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from qikify.helpers import standardize

class SVM(object):
    def train(self, X, gnd, gridSearch = False):
        if gridSearch:
            paramGrid = { 'C': [1, 5, 10, 50, 100], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1] }
            print 'SVM: Grid search using parameters: ', paramGrid
            self.clf = GridSearchCV(SVC(kernel='rbf'), paramGrid, n_jobs=4, fit_params={'class_weight': {1 : 1, -1 : 1}})
        else:
            self.clf = SVC()
        self.scaleDict = dotdict({'mean': X.mean(axis = 0), 'std': X.std(axis = 0)})
        self.clf.fit(standardize(X, self.scaleDict), gnd)

    def predict(self, X):
        return self.clf.predict(standardize(X, self.scaleDict))

    def getTEYL(self, gnd, predicted):
        te = sum(np.logical_and((gnd < 0), (predicted > 0))) * 100.0 / len(gnd)
        yl = sum(np.logical_and((gnd > 0), (predicted < 0))) * 100.0 / len(gnd)
        return [te, yl]




