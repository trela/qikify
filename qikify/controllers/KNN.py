from sklearn.neighbors import KNeighborsClassifier
from qikify.models import Chip
class KNN(object):
    """This class implements the K Nearest Neighborhood Algorithm on a particular 
        chip.
    """
    
    def __init__(self):
        self.chip_LCT_buffer = []
        self.chip_gnd_buffer = []
        self.neigh=KNeighborsClassifier(n_neighbors=5)
        self.X = 0
        self.Y = 0
        self.X_topredict = 0
        self.Y_topredict = 0
        

    def formMatrix(self,chip_arraylist):
        """This function actually forms a matrix consisting of chip parameters and 
            list for gnd values which is used in forming an efficient trained model
            set for furthur use in the prediction model.

            Parameters
            ----------
            chip_arraaylist: array_like
                             Contains a stored array of chip params
        """

        #self.chip_arraaylist=chip_data
        for chip in chip_arraylist:
            self.chip_LCT_buffer.append(chip.LCT.values())
            self.chip_gnd_buffer.append(chip.gnd)
        return  self.chip_LCT_buffer, self.chip_gnd_buffer

    def trainmodel(self,chip_list):
        """Primary execution point where a trained model set is formed from 1000 chip 
            parameters and their gnd values.

            Parameters
            ----------
            chip_list: array_like
                       Contains a stored array of chip params 
        """

        #neigh.fit(self.X,self.Y)
        #self.chips_datalist=chip_list
        self.formMatrix(chip_list)
        self.X = self.chip_LCT_buffer
        self.Y = self.chip_gnd_buffer
        print self.X, self.Y
        #neigh=KNeighborsClassifier(n_neighbors=5)
        self.neigh.fit(self.X,self.Y)
        print "......reached end...."
        #print neigh.predict([[1,0.5]])
        #print neigh.predict([[-1,-0.5]])

    def predict(self,chip_params):
        """This function is another primary point of execution. Here each chip is tested 
            on the basis of the trained model and predict the outcome of the chip using 
            KNN implementation predict method.

            Parameters:
            ----------
            chip_params:array-like
                        Contains a chip's test parameters
        """
        self.X_topredict = chip_params.LCT.values()
        self.Y_topredict = chip_params.gnd
        print self.neigh.predict([[self.X_topredict,self.Y_topredict]])

        


        