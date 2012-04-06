from qikify.models.KNNImplementation import KNNImplementation
from qikify.models import Chip
def test_knn():
	knn=KNNImplementation()
	chip_data1={'ORB_a':1,'ORB_b':1,'gnd':1}
	chip_data2={'ORB_a':-1,'ORB_b':-1,'gnd':-1}
	chip1=Chip(chip_data1,LCT_prefix='ORB')
	chip2=Chip(chip_data2,LCT_prefix='ORB')
	chips=[chip1,chip2]
	print "hi"
	knn.trainmodel(chips)

if __name__ == "__main__":
	test_knn()