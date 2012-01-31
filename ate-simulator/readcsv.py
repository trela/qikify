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

