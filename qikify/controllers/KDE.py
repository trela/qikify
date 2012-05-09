"""Non-parametric kernel density estimation.
"""

import pandas
import numpy as np
from scipy.special import gamma
from qikify.helpers.helpers import standardize
from qikify.helpers.slicesample import slicesample

class KDE(object):
    """This class implements non-parametric kernel density estimation.
    """
    def __init__(self):
        self.bandwidth      = None
        self.Xn             = None
        self.n              = None
        self.d              = None
        self.h              = None
        self.bounds         = None
        self.inner          = None
        self.outer          = None
        self.scale_factors  = None
        self.lambdas        = None
        self.specs          = None
        self.columns        = None
        self.c_d            = None
        
    def fit(self, 
            chips, 
            specs     = None,
            n_samples = 0, 
            counts    = None, 
            a         = 0, 
            bounds    = None):
        """Primary execution point. Run either standard KDE or class-membership
        based KDE. If any of the class-membership based KDE arguments are set,
        it will be run instead of standard KDE.
                
        Parameters
        ----------
        chips : list
            A list of chip model objects.
        
        n_samples : int
            The number of samples to generate.
        
        specs  : qikify.models.Specs, optional
            If using partitioned sampling, boundaries defining pass / critical /
            fail subspaces must be provided.
            
        counts : dict, optional
            If using partitioned sampling, counts dictionary must be provided,
            with three keys: nGood, nCritical, nFail.
                 
        """
        X = pandas.DataFrame([chip.LCT for chip in chips])
        
        self.n, self.d = X.shape
        self.specs     = specs
        self.columns   = getattr(X, 'columns', None)
        
        # Normalize data/bounds        
        self.scale_factors, self.Xn = standardize(X)
        self.bounds = standardize(np.array([X.min(0), X.max(0)]), \
                                  self.scale_factors)
        if bounds is not None:
            self.bounds = standardize(bounds, self.scale_factors)
            
        # Select bandwidth for Epanechnikov kernel (Rule of Thumb, see 
        # Silverman, p.86)
        self.bandwidth = 0.8  # Magic number, default bandwidth scaling factor
        self.c_d     = 2.0 * pow( np.pi, (self.d/2.0) ) / \
                       ( self.d * gamma(self.d/2) )
        self.h       = self._compute_h(self.n, self.d, self.c_d, self.bandwidth)
        self._set_bandwith_factors(a)
        
        # Generate samples
        if counts is None:
            return self._gen_samples(n_samples)
        else:
            print 'KDE: Running on dataset of size n: %d d: %d and \
                generating %d samples.' % (self.n, self.d, sum(counts.values()))
            self._gen_spec_limits(X)
            return self._gen_partitioned_samples(counts)
        
    def _gen_spec_limits(self, X):
        """Default method of generating device samples. We convert spec lims to
        arrays so spec compare during device sample generation is fast. 
        """
        self.inner = np.zeros((2, X.shape[1]))
        self.outer = np.zeros((2, X.shape[1]))
        for i, name in enumerate(X.columns):
            self.inner[:, i] = self.specs.inner[name] \
                               if name in self.specs.inner.keys() \
                               else [-np.inf, np.inf]
            self.outer[:, i] = self.specs.outer[name] \
                               if name in self.specs.outer.keys() \
                               else [-np.inf, np.inf]

    def _gen_samples(self, n_samples):
        """Generate KDE samples.
        """
        Sn = np.vstack([ self._gen_sample() for _ in xrange(n_samples) ])
        sample = standardize(Sn, self.scale_factors, reverse = True)
        return pandas.DataFrame(sample, columns=self.columns)
      
    def _gen_partitioned_samples(self, counts):
        """Generates nCritical critical devices, nGood good devices, nFail
        failing devices, with each region defined by specs.inner /
        specs.outer.
        """

        # Initialize arrays for speed
        Sg, Sc, Sf = np.zeros((counts['nGood'], self.d)), \
                     np.zeros((counts['nCritical'], self.d)), \
                     np.zeros((counts['nFail'], self.d))
        ng, nc, nf = 0, 0, 0
        
        thresh = 0.02
        while ( ng+nc+nf < sum(counts.values()) ):
            sample = standardize(self._gen_sample(), \
                                 self.scale_factors, reverse = True)
            if self._is_good(sample) and ng < counts['nGood']:
                Sg[ng, :] = sample
                ng += 1
            if self._is_failing(sample) and nf < counts['nFail']:
                Sf[nf, :] = sample
                nf += 1
            if self._is_critical(sample) and nc < counts['nCritical']:
                Sc[nc, :] = sample
                nc += 1      
            
            # Prints # generated in each category so we can monitor progress,
            # since this can take a while :)
            if float(ng+nc+nf) / sum(counts.values()) > thresh:
                print 'Ng:%i/%i Nc:%i/%i Nf:%i/%i' % \
                      (ng, counts['nGood'], \
                       nc, counts['nCritical'], \
                       nf, counts['nFail'])
                thresh += 0.02
        print 'Non-parametric density estimation sampling complete.'
        return pandas.DataFrame(np.vstack((Sc, Sg, Sf)), columns=self.columns)


    def _gen_sample(self):
        """Generate a single sample using algorithm in Silverman, p. 143
        """
        
        j = np.random.randint(self.n)
        sample = slicesample(np.zeros(self.d), 1, self._K_e)
        s = self.Xn.ix[j, :] + self.h * self.lambdas[j] * sample

        # Use mirroring technique to deal with boundary conditions.
        # Perhaps we should consider applying boundary kernels here...
        for k in xrange(self.d):
            if (s[k] < self.bounds[0, k]):
                s[k] = self.bounds[0, k] + abs(self.bounds[0, k] - s[k])
            if (s[k] > self.bounds[1, k]):
                s[k] = self.bounds[1, k] - abs(self.bounds[1, k] - s[k])
        return s

    def _set_bandwith_factors(self, a):
        """Estimate local bandwidth factors lambda
        """
        self.lambdas = np.ones(self.n)
        if (a > 0):
            B = [np.log10(self._f_pilot(self.Xn.ix[i, :], self.Xn)) \
                 for i in xrange(self.n)] 
            g = pow(10, sum(B) / self.n)
            self.lambdas = [pow(self._f_pilot(self.Xn.ix[i, :], self.Xn) \
                            / g, -a) for i in xrange(self.n)]

    def _compute_h(self, n, d, c_d, b):
        """Computed here seperately to preserve readability of the equation.
        """
        return b * pow( (8 / c_d * (d + 4) * pow(2 * np.sqrt(np.pi), d) ), \
                        (1.0 / (d + 4))) * pow(n, -1.0 / (d + 4))

    def _K_e(self, t):
        """Epanechnikov kernel.
        """
        return (self.d + 2) / self.c_d * (1 - np.dot(t, t)) / 2 \
                if np.dot(t,t) < 1 \
                else 0

    def _f_pilot(self, x, Xn):
        """Compute pilot density point estimate f(x)"""
        A = [self._K_e( (x - Xn.ix[i, :]) / self.h) for i in xrange(self.n)]
        return (pow(self.h, -self.d) * sum(A)) / self.n

    # =============== Partitioned Sampling Methods =============== 
    def _is_good(self, sample):
        """Returns boolean indicating passing device."""
        return all(sample > self.inner[0, :]) and \
               all(sample < self.inner[1, :])

    def _is_critical(self, sample):
        """Returns boolean indicating critical device."""
        return not (self._is_good(sample) or \
               self._is_failing(sample))

    def _is_failing(self, sample):
        """Returns boolean indicating failing device."""        
        return any(sample < self.outer[0, :]) or \
               any(sample > self.outer[1, :])






