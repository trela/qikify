
# Qikify
      
  MVC framework for adaptive test and semiconductor data analysis
  built on [node.js](http://nodejs.org), [scikits.learn](http://scikit-learn.sourceforge.net/), and
  [numpy](http://numpy.scipy.org/) using Python.


## Installation

  This project is built on and requires the following software:  
  
  * python 2.7.1
  * numpy 1.5.1
  * scipy 0.9.0
  * node.js 0.5.0-pre

  Once the above are installed, just clone this github repository with

     git clone git://github.com/natekupp/mvc-framework.git

  to get started.

## Features

  * Intuitive data model
  * Modular support for "controllers" to implement machine-learning analysis techniques
  * Web-based interaction with machine-learning tasks running server-side via [node.js](http://nodejs.org)

## Example
Here's a simple example to get you started:

     from models.Specs import *
     from models.Dataset import *
     from controllers.svm import SVM
	 
	 specs = Specs('/path/to/specs')
	 svm   = SVM.SVM()
	 
	 # Get training data
	 trainingData  = Dataset('/path/to/training/set').computePF(specs); trainingData.printSummary()
	 
	 # Train SVM
	 svm.train(trainingData['raw'].data, trainingData['raw'].gnd, gridSearch=True)
	 
	 # Predict
	 testData  = Dataset('/path/to/test/set').computePF(specs)
	 predicted = svm.predict(testData['raw'].data)
	 print svm.getTEYL(testData['raw'].gnd, predicted))

A more involved example can be found in `framework/example.py`.

## Contributors

The following are the major project contributors.

  * Nate Kupp ([natekupp](https://github.com/natekupp))

## License 

(The MIT License)

Copyright copy; 2011 Nathan Kupp, Yale University.

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

