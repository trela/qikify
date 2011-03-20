import csv
from numpy import * 

# Compare data to lsl, usl and return +1/-1 label vector
def compareToSpecs(data, lsl, usl):
	result = ones(size(data))
	if ~isnan(lsl):
		result = (data >= lsl)
	if ~isnan(usl):
		result = logical_and(result, data <= usl)
	return bool2symmetric(result)
	
	
# Write mat to filename as a csv.
def csvWriteMatrix(filename, mat):
	out  = csv.writer(open('../data/' + filename, 'wb'))
	for row in mat:
		out.writerow(row)
		
		
# Use dotdict to replace dictionaries. This enables dict.property access.
class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


# Changes True/False data to +1/-1 symmetric.
def bool2symmetric(data):
	return array((data - 0.5) * 2.0, dtype = int)
	
	
def scale(data, scaleDict):
	return (data - scaleDict.mean) / scaleDict.std