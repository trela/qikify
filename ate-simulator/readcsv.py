#!/usr/bin/python
############################################
'''
This python file is able to extract all the infor mation from a csv file and is able to store it in a dictionary. 
The dictiobary contains the different measurements specification as the keys. 
All the corresponding data of the the specification are stored in a list format as the value of that corresponding key. 
'''
############################################

#Read CSV file and store it in a dictionary

import csv
import re
#import 
from collections import defaultdict
linereader=csv.reader(open('Data/wafer1.csv','r'))
#print linereader.readline()
#data=[row for row in linereader]
#print data
rownum=0
#d={}
table= defaultdict(list)
filename="text.txt"
for row in linereader:
	#print "hi"
	if rownum==0:
		header=row
	else:
		datalist=row
	rownum+=1
	if rownum>1:
		size=len(header)
		
		for i in range(1,size):
			table[header[i-1]].append(row[i-1])
			#d.update([table])
				
		
#print header
#ssplitter=re.compile(",")
#print header
#print header[1]
#size=len(header)
print size
print table.get(header[1])
#FILE=open(filename,"w")
#FILE.writelines(table)
#FILE.close()

