#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='qikify',
    version='0.2.0',
    description='Qikify: A MVC Adaptive Test Solution',
    author='Nathan Kupp',
    author_email='nathan.kupp@yale.edu',
    url='http://github.com/trela/qikify',
    license='MIT',
    scripts=['qikify/bin/qikify'],
    packages = find_packages(),
    install_requires=[
        'setuptools',
        'numpy', 
        'scipy', 
        'matplotlib',
        'pandas',
        'scikit-learn',
        'pyzmq', 
        'msgpack-python'
    ]
)
