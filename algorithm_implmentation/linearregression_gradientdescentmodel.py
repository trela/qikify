import numpy as np
import matplotlib.pyplot as plt

class linearregression_gradientdescentmodel(object):
	def __init__(self):
		self.chip_theta = []
		self.chip_targetvalues = []
		self.sumofx_i=0
		self.alpha=1e-6
		self.m=0
		#self.rows=list()
		#self.thetas=list()
		self.estimated_theta=list()
		#self.inittheta0=0
		self.no_features=0
		self.feature_matrix=[[]]
		self.int_feature_matrix=[[]]
		self.sum=0
		self.n1=list()
		self.n2=list()

	def form_hypothesis(self):
		init_thetas=list()
		datafile = open("dataset.txt",'r')
		for line in datafile:
			line=line.split("\n")[0]
			self.m+=1
			featurelist=line.split('  ')
			self.no_features=len(featurelist)

			print "featurelength %i" %self.no_features
			if self.m==1:
				self.feature_matrix[0]=featurelist
			else:
				self.feature_matrix.append(featurelist)
		print self.feature_matrix
		print self.m
		featurelength=len(featurelist)
		self.int_feature_matrix=np.array(self.feature_matrix,dtype=float)
		#self.sum_y=self.calculate_sum_colomn(self.int_feature_matrix,len(featurelist)-1)
		for j in range(0,len(featurelist)):
			random_theta=np.random.random()
			self.estimated_theta.append(random_theta)
		
		for n in range(0,1000):
			#coloumn_list=list()
			sum_coloumn=list()
		#	hypo_sum=0
		#	linear_sum=0
		#	calsum=0
		#	iteration=0	

			for j in range(0,len(featurelist)):
				hypo_sum=0
				linear_sum=0
				calsum=0
				diff=0		
				for y in range(0,self.m):
					#if y==0:
					value_x=list()
					for x in range(0,len(featurelist)):
						hypo_sum=self.calculate_sum(calsum,self.estimated_theta,self.int_feature_matrix,y,x)
						#coloumn_list+str(x)=list()
						#coloumn_list+str(x)=self.int_feature_matrix[:,x]
					diff+=pow(hypo_sum-self.int_feature_matrix[y][featurelength-1],2)
					#print 'cost value'
					#print cost
					#print 1/float(self.m)
					if j==0:
						linear_sum+=(hypo_sum-self.int_feature_matrix[y][featurelength-1])
					else:
						#name=coloumn_list+str(j)
						#print name
						linear_sum+=(hypo_sum-self.int_feature_matrix[y][featurelength-1])*self.int_feature_matrix[y][j]
					#print self.int_feature_matrix[y][featurelength-1]
				sum_coloumn.append(linear_sum)
			cost=(1/float(2*self.m))*diff
			print 'cost value..........'
			print cost
			self.n1.append(n)
			self.n2.append(cost)
			costlength=len(self.n2)
			n3=self.n2[costlength-2]
			#print n3
			if costlength>1 and cost>n3:
				#val=self.alpha
				self.alpha=self.alpha/float(10)
			#plt.show()
			#print linear_sum
			for k in range(0,featurelength):
				temp=self.estimated_theta[k]-self.alpha*(1/float(self.m))*sum_coloumn[k]
				self.estimated_theta.remove(self.estimated_theta[k])
				self.estimated_theta.insert(k,temp)
				
			print self.estimated_theta
		plt.plot(self.n1,self.n2)
		plt.show()
	def calculate_sum(self,hypo_sum,thetas,feature_matrix,y,x):
		if x==0:
			#sum=0
			hypo_sum=thetas[x]
			#htheta=htheta+thetas[x+1]*float(feature_matrix[y][x])
		else:
			#print "y value %f"%feature_matrix[y][featurelength-1]
			hypo_sum+=thetas[x]*self.int_feature_matrix[y][x-1]
		#rows.append(featurelist[x])
		return hypo_sum

	def calculate_sum_colomn(self,matrix,i):
		#sumofx=0
		coloumn_list=list()
		print 'in sum............'
		print i
		#for i in range (0,self.m-1):
		#import pdb; pdb.set_trace()
		#import pdb; pdb.set_trace()
		coloumn_list=matrix[:,i]
		return np.sum(np.array(coloumn_list))

if __name__ == "__main__":
	l_reg=linearregression_gradientdescentmodel()
	l_reg.form_hypothesis()