
# Qikify
      
Qikify is a Model-View-Controller framework for addressing challenging semiconductor data analysis and machine learning tasks. Qikify is built in Python using numpy, but learning Qikify should be easy for anyone familiar with MATLAB or R.

The objective of this project is to simplify the task of working with semiconductor data in production environments.

Using the MVC pattern partitions your application into three distinct components, each with very specific responsibilities. 

For a first release, we are targeting CSV-based data and applying basic machine learning algorithms to implement adaptive test applications. After an initial release, our roadmap includes moving to a Hadoop HDFS/HBase backend for data storage, rewriting some of the key algorithms to support Hadoop MapReduce implementations, and building more general tools to address semiconductor data analysis tasks.


# Organization

As an MVC framework, Qikify aims to define clear design patterns for implementing data analysis tasks. Semiconductor datasets are abstracted as ___models___, machine learning algorithms are defined in ___controllers___, and real-time traces of running algorithms are observed in ___views___. Finally, these MVC components are assembled as ___recipes___; several example recipes will be included with the framework covering basic machine learning tasks.


## Models

The atomic model used in our framework is the `Chip` model, encapsulating chip-level data. Higher level (wafer or lot) abstractions are clearly possibly, but we have found abstracting data at the chip-level to be the best for maintaining clean interfaces between blocks. To generate `Chip` objects, an `ATESimulator` recipe is provided to simulate automated test equipment. This ATE simulator takes raw CSV data and periodically emits chip objects.

## Controllers
A large number of controllers are provided with the Qikify framework. These controllers aim to provide simple APIs, usually defining a standard `controller.run()` method.

## Views
In Qikify, a view server recipe is provided. The view server listens for JSON from recipes and controllers, and then forwards that on to any connected web clients. Some client-side javascript parses the JSON and turns it into graphical representations.


# Installation

  This project is built on and requires the following software:  
  
  * [python 2.6.6+](http://www.python.org/)
  * [numpy 1.6.1+](http://numpy.scipy.org/)
  * [scipy 0.9.0+](http://www.scipy.org/)
  * [sklearn 0.10+](http://scikit-learn.org/stable/)
  * [pandas 0.7.3+](http://pandas.pydata.org/)
  * [ZeroMQ](http://www.zeromq.org/)
  * [msgpack](http://msgpack.org/)
  
Depending on your platform, installing these dependencies is usually straightforward. Once python is installed, `pip install [packagename]` will do the trick, with the notable exception of numpy/scipy. These libraries are built on fortran ATLAS/LAPACK and usually will not install cleanly from PyPI; binaries should be downloaded directly from the [project site](http://www.scipy.org/Download).

Once the above are installed, install qikify with:

    git clone git://github.com/trela/qikify.git
    cd qikify
    python setup.py install

to get started with the code.


## Contributors

The following are the major project contributors.

  * Nate Kupp ([natekupp](https://github.com/natekupp))
  * Abhishek Basu ([abhishekingithub](https://github.com/abhishekingithub))
  * Ke Huang ([hkhk](https://github.com/hkhk))

## License 

(The MIT License)

Copyright &copy; 2011-2012 Nathan Kupp, Yale University.

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

