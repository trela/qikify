from distutils.core import setup, Extension
 
module1 = Extension('slicesample', sources = ['slicesample.c'])
 
setup (name = 'Slicesample',
        version = '1.0',
        description = 'This is a C version of slicesample, built for speed.',
        ext_modules = [module1])
