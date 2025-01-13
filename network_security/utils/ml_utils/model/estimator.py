import os
import sys
import numpy as np
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME 

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x) -> np.ndarray:
        try:
            x_trans = self.preprocessor(x)
            y_hat = self.model.predict(x_trans)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)

