from sklearn.neighbors import KNeighborsClassifier
from qikify.models import Chip
class KNNImplementation(object):
	def __init__(self):
		self.chip_LCT_buffer=[]
		self.chip_gnd_buffer=[]
		neigh=KNeighborsClassifier(n_neighbors=5)
		

	def formMatrix(self,chip_arraylist):
		#self.chip_arraaylist=chip_data
		for chip in chip_arraylist:
			self.chip_LCT_buffer.append(chip.LCT.values())
			self.chip_gnd_buffer.append(chip.gnd)
		return 	self.chip_LCT_buffer, self.chip_gnd_buffer

	def trainmodel(self,chip_list):
		#neigh.fit(self.X,self.Y)
		#self.chips_datalist=chip_list
		self.formMatrix(chip_list)
		self.X=self.chip_LCT_buffer
		self.Y=self.chip_gnd_buffer
		print self.X, self.Y
		#neigh=KNeighborsClassifier(n_neighbors=1)
		neigh.fit(self.X,self.Y)
		print "......reached end...."
		print neigh.predict([[1,0.5]])
		print neigh.predict([[-1,-0.5]])

	def predict(self,chip_params):
		self.X_topredict=chip_params.LCT.values()
		self.Y_topredict=chip_params.gnd
		print neigh.predict([[self.X_topredict,self.Y_topredict]])

		


		