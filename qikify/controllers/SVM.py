#!/usr/bin/python
'''
Copyright (c) 2011 Nathan Kupp, Yale University.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import numpy as np

from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from scikits.learn.metrics import confusion_matrix
from scikits.learn.svm import SVC
from helpers import *

class SVM(object):
    def train(self, X, gnd, gridSearch = False):
        #print 'SVM: Training.'
        self.gridSearch = gridSearch
        if self.gridSearch:
            paramGrid = { 'C': [1, 5, 10, 50, 100], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1] }
            print 'SVM: Grid search using parameters: ', paramGrid
            self.clf = GridSearchCV(SVC(kernel='rbf'), paramGrid, n_jobs=4, fit_params={'class_weight': {1 : 1, -1 : 1}})
        else:
            self.clf = SVC()
        self.scaleDict = dotdict({'mean': X.mean(axis = 0), 'std': X.std(axis = 0)})
        self.clf.fit(scale(X, self.scaleDict), gnd)
        #print 'SVM: Training complete.'

    def predict(self, X):
        return self.clf.predict(scale(X, self.scaleDict))

    def getTEYL(self, gnd, predicted):
        te = sum(np.logical_and((gnd < 0), (predicted > 0))) * 100.0 / len(gnd)
        yl = sum(np.logical_and((gnd > 0), (predicted < 0))) * 100.0 / len(gnd)
        return [te, yl]
