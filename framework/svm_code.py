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

from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from scikits.learn.metrics import confusion_matrix
from scikits.learn.svm import SVC


# First pass integration of SVM code
def runSVM():
	dataTrain 	  = Dataset('~/Desktop/svm/xTrain.csv', hasHeader = False)
	dataTrain.gnd = Dataset('~/Desktop/svm/yTrain.csv', hasHeader = False).data
	dataTest 	  = Dataset('~/Desktop/svm/xTest.csv',  hasHeader = False)
	dataTest.gnd  = Dataset('~/Desktop/svm/yTest.csv',  hasHeader = False).data

	dataTrain.printSummary()
	dataTest.printSummary()

	scaleDict = dotdict({'mean': dataTrain.data.mean(axis = 0), 
						  'std': dataTrain.data.std(axis = 0)})

	param_grid = {
	 'C': [1, 5, 10, 50, 100],
	 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1],
	}
	clf = GridSearchCV(SVC(kernel='rbf'), param_grid, fit_params={'class_weight': {1 : 1, -1 : 100}})
	clf = clf.fit(scale(dataTrain.data, scaleDict), dataTrain.gnd)
	print "Best estimator found by grid search:"
	print clf.best_estimator

	y_pred = clf.predict(scale(dataTest.data, scaleDict))
	print classification_report(dataTest.gnd, y_pred)
	print confusion_matrix(dataTest.gnd, y_pred)



## Simple pred
#clf = svm.SVC()
#clf.fit(scale(dataTrain.data, scaleDict), dataTrain.gnd)
#gndPredicted = clf.predict(scale(dataTest.data, scaleDict))

## Something like this to use bare metal libsvm. Still haven't figured this out.
#sys.path.append('./libsvm')
#from svm import *
#x = scale(dataTrain.data, scaleDict)
#px = svm_problem(dataTrain.gnd, x.tolist())
#pm = svm_parameter()
#v  = svm_model()
#v.predict(scale(dataTest.data, scaleDict).tolist())
