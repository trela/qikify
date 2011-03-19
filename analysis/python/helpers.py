import csv
from numpy import * 

def compareToSpecs(data, lsl, usl):
	result = ones(size(data))
	if ~isnan(lsl):
		result = data >= lsl
	if ~isnan(usl):
		result = logical_and(result, data <= usl)
	return result
	
	
def csvWriteMatrix(filename, mat):
	out  = csv.writer(open('../data/' + filename, 'wb'))
	for row in mat:
		out.writerow(row)