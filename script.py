import numpy as np 
import pickle as pkl 

class Predictor:

    def __init__(self):
        self.model = pkl.load(open('model_file.pkl', 'rb'))

    def predict(self, values):
        values = np.asarray(values)
        prediction = self.model.predict(values.reshape(1,-1))
        return prediction
