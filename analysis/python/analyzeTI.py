import csv, os, glob, numpy, sys

sys.path.append('./libsvm')

from Dataset_TI import *  
from Specs import *
from helpers import *
from svm import *


if __name__ == "__main__":
	
	dataDir	  = '/Users/nathankupp/Research Data/TI/'
	dataFiles = glob.glob(dataDir + 'all/*.csv')
	specs     = Specs(dataDir + 'specsCleanedNoORBiT.csv')
	baseData  = Dataset_TI(dataFiles[0])
	baseData.initSubsetIndices(specs)
	baseData.printSummary()
	
	#csvWriteMatrix('pfMat_Python.csv', baseData.pfMat)
	#csvWriteMatrix('data_Python.csv', baseData.sData)
	
	
	
	