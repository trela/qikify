"""Qikify: specs.
"""

import numpy as np
import pandas
from qikify.helpers.term_helpers import colors

class Specs(object):   
    """Qikify specs model.
    """ 
    
    def __init__(self, filename = None, specs=None):
        """Read in specs from `filename` and create {specname: [lsl,usl]}
        dictionary. Alternatively, can provide specs directly. 
        """
        self.inner = None
        self.outer = None
        self.col = colors()
        
        if filename is not None:    
            self.specs = pandas.read_csv(filename)
            try:
                # try to force floating-point data type
                self.specs = pandas.DataFrame(self.specs, dtype=float) 
            except:
                # oh well, we tried
                pass 
                
        elif specs is not None:
            self.specs = specs
        else:
            raise Exception('Specs not provided.')
        
        ## NaN limits --> +/- infinity

        # lower spec limits
        self.specs.ix[0, np.isnan(self.specs.ix[0, :])] = -np.inf 

        # upper spec limits 
        self.specs.ix[1, np.isnan(self.specs.ix[1, :])] = np.inf   

        
    def __getitem__(self, key):
        return self.specs[key]

    
    def __str__(self):
        """Print a summary of the specifications.
        """
        output = ''
        for name in self.specs.columns:
            spec_lims_str = \
                [str(x) for x in self.specs[name].tolist() if not np.isnan(x)]
            output += '%s %27s %s: \t' % (self.col.WARNING, name, self.col.ENDC)
            output += ' <> '.join(spec_lims_str) + '\n'
        return output

    def gen_crit_region(self, k_i, k_o):
        """Takes specification boundary and generates two boundaries to define
        'critical' device region.
        
        Parameters
        ----------
        k_i : Inner critical region multiplier.
        k_u : Outer critical region multiplier.
        """
        
        self.inner, self.outer = {}, {}
        for name in self.specs.columns:
            lsl, usl   = self.specs[name]
            mu         = np.mean([lsl, usl])

            self.inner[name] = \
                np.array([mu - k_i * abs(mu-lsl), mu + k_i * abs(mu-usl)])

            self.outer[name] = \
                np.array([mu - k_o * abs(mu-lsl), mu + k_o * abs(mu-usl)])

        return self
    
    def compute_pass_fail(self, data):
        """Compare a pandas Series or DataFrame structure to specification
        limits defined by this spec class instance.
        
        Parameters
        ----------
        data : Contains data stored in Series or DataFrame.
        """
        if isinstance(data, pandas.Series):
            lsl, usl = self[data.name]
            return data.apply(lambda x: x >= lsl and x <= usl)
            
        if isinstance(data, pandas.DataFrame):
            pf_mat = pandas.DataFrame(np.ones(data.shape, dtype=bool), \
                                      columns=data.columns)
                                      
            for j in xrange(data.shape[1]):
                lsl, usl = self[data.columns[j]]
                pf_mat.ix[:, j] = \
                    data.ix[:, j].apply(lambda x: x >= lsl and x <= usl)

            return pf_mat
            
        else:
            raise ValueError('Cannot compare non-pandas data structure.')
            
            
