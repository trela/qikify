#!/usr/bin/python
'''
Copyright (c) 2011 Nathan Kupp, Yale University.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import csv
from ConfigParser import ConfigParser
from glob import glob
from random import sample

import qikify.helpers.general as helpers
from qikify.models.Specs import Specs
from qikify.models.DatasetTI import DatasetTI
from qikify.controllers.kde import KDE
from qikify.controllers.lsfs import LSFS
from qikify.controllers.svm import SVM

K_INNER, K_OUTER = 5.5/6, 6.5/6

config = ConfigParser(); config.read('settings.conf')
specs  = Specs(config.get('Settings', 'specFile')).genCriticalRegion(K_INNER, K_OUTER)
lsfs   = LSFS.LSFS()
kde    = KDE.KDE()
svm    = SVM.SVM()

if __name__ == "__main__":
    dataFiles = glob(config.get('Settings', 'dataFiles'))
    baseData  = DatasetTI(dataFiles[0])
    print baseData
    
    





