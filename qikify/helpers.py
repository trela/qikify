"""Qikify helpers.
"""

import numpy as np
import scipy, pandas, logging, os

def create_logger(logmodule):
    """Creates a logger for 'logmodule', enabling qikify controllers/recipes to
    log to text output files. Useful for generating data that later is used in
    views.
    """
    
    logger = logging.getLogger(logmodule)
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    try:
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read(os.path.expanduser('~/.qikifyrc'))
        logdir = config.get('Logging', 'logdir')
    except IOError:
        logdir = '/tmp/qikify/test'

    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logfile = os.path.join(logdir, '%s.log' % logmodule)
    
    # create file log handler
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.INFO)
    
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # create formatter and add it to the handlers
    formatter = \
       logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger



def bool2symmetric(data):
    """Changes True/False data to +1/-1 symmetric.
    """
    return np.array(( data - 0.5 ) * 2.0, dtype = int)


def standardize(X, scale_dict = None, reverse = False):
    """Facilitates standardizing data by subtracting the mean and dividing by
    the standard deviation. Set reverse to True to perform the inverse 
    operation.
    
    Parameters
    ----------
    X : numpy ndarray, or pandas.DataFrame
        Data for which we want pareto-optimal front.
    scale_dict: dict, default None
        Dictionary with elements mean/std to control standardization.
    reverse: boolean, default False
        If this flag is set, the standardization will be reversed; e.g.,
        we take a dataset with zero mean and unit variance and change to
        dataset with mean=scaleDict.mean and std=scaleDict.std.
    
    Examples
    --------
    >>> Xstd, scale_dict = standardize(X)
        
    """
    if reverse:
        return (X * scale_dict['std']) + scale_dict['mean']
    elif scale_dict is None:
        scale_dict = {'mean': X.mean(0).tolist(), \
                       'std': X.std(0).tolist()}
        return scale_dict, (X - scale_dict['mean']) / scale_dict['std']
    else:
        return (X - scale_dict['mean']) / scale_dict['std']



def set_submat(X, D, ind):
    """Set a submatrix of X defined by the index ind to values in D. 
    That is:
             [0, 0, 0]
         X = [0, 0, 0]   D = [1 2] ind = [0 1]
             [0, 0, 0]       [3 4]
    Gives:
             [1, 2, 0]
         X = [3, 4, 0]
             [0, 0, 0]
    """
    for i, row in enumerate(ind):
        X[row, ind] = D[i, :]


def gen_max_mat(A):
    """Takes a square matrix A and computes max(A, A').
    """
    ind = (A.T - A) > 0
    A[ind] = A.T[ind]
    return A
    

def zero_diag(X):
    """Set the diagonal of a matrix to all zeros.
    
    Parameters
    ----------
    X : numpy ndarray
        Matrix on which to zero out the diagonal.
        
    Examples
    --------
    Xp = zero_diag(X)
    
    """
    return X - np.diag(np.diag(X))


def get_pareto_front(data):
    """Extracts the 2D Pareto-optimal front from a 2D numpy array.
    
    Parameters
    ----------
    data : numpy ndarray, or pandas.DataFrame
        Data for which we want pareto-optimal front.
    
    Examples
    --------
    p = get_pareto_front(data)
    
    """
    dflags = np.ones(data.shape[0], dtype=bool)
    for i in xrange(data.shape[0]):
        point = data[i, :]
        for j in xrange(data.shape[0]):
            if i == j:
                continue
            if np.all(point > data[j, :]):
                dflags[i] = False
    return np.array(data[dflags, :])


def is1D(data):
    """Determine if data is 1-dimensional.
    
    """
    return data.shape[0] == np.size(data)


def partition(data, threshold=0.5, verbose = False):
    """Partitions data into training and test sets. Assumes the last column of
    data is y.
    
    Parameters
    ----------
    data : numpy ndarray, or pandas.DataFrame
        Data to partition into training and test sets.
    threshold : float
        Determines ratio of training : test.
        
    Examples
    --------
    >>> xtrain, ytrain, xtest, ytest = partition(data)
        
    """
    
    if data.ndim != 2:
        raise Exception, 'data must be 2-dimensional'

    nrow, ncol = data.shape
    
    # create boolean vector identifying rows in training/test sets.
    index = np.random.sample(nrow)
    train_index = index < threshold
    test_index = index >= threshold
    
    if isinstance(data, pandas.DataFrame):        
        xtrain = data.ix[train_index, :ncol-1]
        ytrain = data.ix[train_index, ncol-1]
        xtest  = data.ix[test_index, :ncol-1]
        ytest  = data.ix[test_index, ncol-1]
    elif isinstance(data, np.ndarray):
        xtrain = data[train_index, :-1]
        ytrain = data[train_index, -1]
        xtest  = data[test_index, :-1]
        ytest  = data[test_index, -1]
    else:
        raise Exception, 'data must be numpy.ndarray or pandas.DataFrame'
    
    if verbose:
        print 'Randomly partitioned data, with threshold={0}'.format(threshold)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('xtrain', *xtrain.shape)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('ytrain', ytrain.size, 1)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('xtest', *xtest.shape)
        print '{:<10} nrow: {:<4} ncol: {:<4}'.format('ytest', ytest.size, 1)
        
    return xtrain, ytrain, xtest, ytest


def nmse(yhat, y, min_y=None, max_y=None):
    """Calculates the normalized mean-squared error. 
    
    Parameters
    ----------
    yhat : 1d array or list of floats
        estimated values of y
    y : 1d array or list of floats
        true values
    min_y, max_y : float, float
      roughly the min and max; they do not have to be the perfect values of min
      and max, because they're just here to scale the output into a roughly
      [0,1] range

    Examples
    --------
    nmse = nmse(yhat, y)
    
    """
    #base case: no entries
    if len(yhat) == 0:
        return 0.0
    
    #base case: both yhat and y are constant, and same values
    if (max_y == min_y) and (max(yhat) == min(yhat) == max(y) == min(y)):
        return 0.0
    
    #main case
    assert max_y > min_y, 'max_y=%g was not > min_y=%g' % (max_y, min_y)
    yhat_a, y_a = np.asarray(yhat), np.asarray(y)
    y_range = float(max_y - min_y)
    try:
        result = np.sqrt(np.mean(((yhat_a - y_a) / y_range) ** 2))
        if scipy.isnan(result):
            return np.Inf
        return result
    except ValueError:
        print 'Invalid result %d' % (result)
        return np.Inf


def computeR2(yhat, y):
    """Computes R-squared coefficient of determination.
    
       R2 = 1 - sum((y_hat - y_test)**2) / sum((y_test - np.mean(y_test))**2)

    Parameters
    ----------
    yhat : 1d array or list of floats -- estimated values of y
    y : 1d array or list of floats -- true values
    
    Examples
    --------
    r2 = computeR2(yhat, y)
    
    """
    return np.corrcoef(yhat, y)[0, 1]**2
    

def compute_corr_coefs(X, y):
    """Returns the correlation coefficients between X and y, along with the
    arg-sorted indices of ranked most-correlated X-to-y vars. 
    """
    corr_coef = np.array([np.corrcoef(X[:, i], y)[0, 1] \
                      for i in xrange(X.shape[1])])
                                            
    return corr_coef, np.argsort(-abs(corr_coef))

                
            
def compute_te_yl(gnd, predicted):
    """Report test escapes / yield loss test metrics due to using the 
    trained classifier.
    """
    test_escapes = \
        sum(np.logical_and((gnd < 0), (predicted > 0))) * 100.0 / len(gnd)
    yield_loss = \
        sum(np.logical_and((gnd > 0), (predicted < 0))) * 100.0 / len(gnd)
    return [test_escapes, yield_loss]
    


