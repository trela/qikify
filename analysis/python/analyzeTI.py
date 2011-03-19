import csv, os, glob, numpy, sys, ConfigParser

sys.path.append('./libsvm')

from Dataset_TI import *  
from Specs import *
from helpers import *
from svm import *


if __name__ == "__main__":
	config = ConfigParser.RawConfigParser()
	config.read('settings.conf')
	
	dataFiles = glob.glob(config.get('Settings', 'dataFiles'))
	specs     = Specs(config.get('Settings', 'specFile'))
	
	baseData  = Dataset_TI(dataFiles[0])
	baseData.initSubsetIndices(specs)
	baseData.printSummary()

	
	
	