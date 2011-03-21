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


class Specs:
	specs = {}
	names = []
	
	def __init__(self, filename):
	    """This class retrieves specification limits from the file 
	    filename. Note that it expects the following format for each column: 
        
	             Col. 1            Col. 2                        
	       [ Test_Name     ]     [ Test_Name     ]                 
	       [ LSL           ]     [ LSL           ]     ...         
	       [ USL           ]     [ USL           ]                 

	    Args:
	    filename: The name of the CSV-formatted spec limit file.    
    
	    Returns:
	    Creates the dictionary { test_ID: [LSL, USL], ... } 
	    """
    
	    fileh 	  	= open(filename, 'rU')
	    specReader 	= csv.reader(fileh)
	    self.names 	= specReader.next()
	    LSL   		= specReader.next()
	    USL   		= specReader.next()

	    for i, limit in enumerate(zip(LSL, USL)):
			# Use this lambda function because float() fails on empty string, i.e. the 
			# non-existent spec limit.
	    	lsl, usl = map(lambda x: float(x) if x else float('nan'), limit)
	        self.specs[self.names[i]] = [lsl, usl]
        
	    fileh.close()

    
	def __getitem__(self, key):
		return self.specs[key]
    
    
    
