import sys

from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainPipeline
from network_security.exception.exception import NetworkSecurityException


if __name__ == "__main__":
    try:
        train_pipeline = TrainPipeline()
        modelTrainArtifact = train_pipeline.initiate_pipeline() 
        print(modelTrainArtifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


