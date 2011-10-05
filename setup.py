#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='qikify',
      version='0.1',
      description='Qikify: A MVC Adaptive Test Solution',
      author='Nathan Kupp',
      author_email='nathan.kupp@yale.edu',
      url='http://github.com/trela/qikify',
      license='MIT',
      packages = find_packages('qikify'),  # include all packages under src
      package_dir = {'':'qikify'},   # tell distutils packages are under src
     )