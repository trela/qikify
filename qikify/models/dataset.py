"""
.. warning:: Deprecated in version 0.2.

"""
import numpy as np
import gzip, StringIO, sys, os, csv, pandas

from qikify.helpers import is1D
from qikify.term_helpers import colors
from .dotdict import dotdict

class Dataset(dotdict): 
    """This class is the fundamental data structure of the Qikify framework.
    """
    def __init__(self, filename=None, files=None, dataset=None):
        """Dataset can be constructed from:
        filename:  individual file to load
        files:     list of files to concatenate and load
        dataset:   an existing dataset
        """
        if filename is not None:
            self.raw = self._loadfile(filename)
            
        elif files is not None:
            data = self._loadfile(files[0])
            for filename in files[1:]:
                newdata = self._loadfile(filename)
                data = pandas.concat([data, newdata], axis=0, ignore_index=True)
            self.raw = data
            
        elif dataset is not None:
            self.raw = dataset
            
        else:
            self.raw = None

    def _loadfile(self, filename):
        filetype = filename.split('.')[-1]
        if filetype == 'csv':
            data = pandas.read_csv(filename)
        elif filetype == 'gz':
            with gzip.open(filename, 'r') as f:
                data = pandas.read_csv(StringIO.StringIO(f.read())) 
        else:
            raise Exception("Wrong file type, expected .csv or .csv.gz.")
        return data
        
    def __repr__(self):
        """Print a summary of the dataset."""
        output = colors().GREEN + \
               '===============================================\n' + \
               'Dataset                         #Rows #Cols    \n' + \
               '===============================================\n' + colors().ENDC
        for key in self.keys():
            if is1D(self[key]):
                output += '%-30s %5d %5d\n' % (key, self[key].shape[0], 1)
            else:
                output += '%-30s %5d %5d\n' % (key, self[key].shape[0], self[key].shape[1])
        return output



    