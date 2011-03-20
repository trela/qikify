import csv, os, glob, numpy, sys, ConfigParser
from Dataset import *
from Dataset_TI import *
from Specs import *
from helpers import *

from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from scikits.learn.metrics import confusion_matrix
from scikits.learn.svm import SVC


'''
if __name__ == "__main__":
	config = ConfigParser.RawConfigParser()
	config.read('settings.conf')
	
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs(config.get('Settings', 'specFile'))
	
	baseData  = Dataset_TI(dataFiles[0])
	baseData.initSubsetIndices(specs)
	baseData.printSummary()

'''


# First pass integration of SVM code
dataTrain 	  = Dataset('/Users/nathankupp/Desktop/svm/xTrain.csv', hasHeader = False)
dataTrain.gnd = Dataset('/Users/nathankupp/Desktop/svm/yTrain.csv', hasHeader = False).data
dataTest 	  = Dataset('/Users/nathankupp/Desktop/svm/xTest.csv',  hasHeader = False)
dataTest.gnd  = Dataset('/Users/nathankupp/Desktop/svm/yTest.csv',  hasHeader = False).data

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
