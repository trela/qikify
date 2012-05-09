from sklearn.neighbors import KNeighborsClassifier

class KNN(object):
    """This class implements the K Nearest Neighborhood Algorithm.
    """
    
    def __init__(self, n_neighbors=5):
        self.knnmodel = KNeighborsClassifier(n_neighbors)

    def fit(self, chips):
        """Primary execution point where a trained model set is formed from chip 
            parameters and their gnd values.

            Parameters
            ----------
            chip_list: list
                Contains a stored array of Chip objects 
        """
        X = [chip.LCT.values() for chip in chips]
        y = [chip.gnd for chip in chips]    
        self.knnmodel.fit(X, y)
        
        
    def predict(self, chip):
        """Here each chip is tested on the basis of the trained model and 
        predicts the outcome of the chip using KNN implementation predict 
        method.

            Parameters:
            ----------
            chip: chip model object
                Contains a chip's test parameters
        """
        return self.knnmodel.predict(chip.LCT.values())

        


        