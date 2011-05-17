from distutils.core import setup, Extension
import numpy as np                           # <---- New line
 
module1 = Extension('_C_slicesample', sources = ['C_slicesample.c'])
 
setup (name = 'slicesample',
        version = '1.0',
        include_dirs = [np.get_include() + '/numpy'], 
        description = 'This is a C version of slicesample, built for speed.',
        ext_modules = [module1])
