import numpy as np 
import pickle as pkl 

class Predictor:
    """
    This class has the methods for predicting burn rate from different stats arranged from the user.
    """
    def __init__(self):
        """
        Constructor which loads the model to the self.model object.
        """
        self.model = pkl.load(open('model_file.pkl', 'rb'))

    def predict(self, values):
        """
        Function which calculates the burn rate by considering the following features:
        1. Gender(0 - male, 1 - female)
        2. Company Type(0 - Service, 1 - Product)
        3. Work from home setup available(0 - No, 1 - Yes)
        4. Designation(0 - 3 increasing level)
        5. Resource Allocation(hours given in work)
        6. Mental Fatigue Score(0 - 1 )

        Parameters
        ----------
        values : list containing all the mentioned values

        Return
        ---------
        prediction : Predicted burn rate
        """
        values = np.asarray(values)
        prediction = self.model.predict(values.reshape(1,-1))
        return prediction
