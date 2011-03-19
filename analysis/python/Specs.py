#!/usr/bin/env python

#    Copyright (C) 2009 Nathan Kupp.  All rights reserved.
# 
# This file is part of my codebase.
#
# This is free software; you can redistribute it and/or
# modify it under the terms of the version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This software is provided AS-IS with no warranty, either express or
# implied. That is, this program is distributed in the hope that it will 
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA, 02110-1301.
# 


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
    
    
    
