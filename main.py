import sys

from network_security.logging.logger import logging
from network_security.components.model_trainer import ModelTrainer
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig 
from network_security.entity.config_entity import DataTransformationConfig, ModelTrainerConfig

if __name__ == "__main__":
    try:
        
        trainPipConfig = TrainingPipelineConfig()
        dataIngConfig = DataIngestionConfig(trainPipConfig)
        dataIngestion = DataIngestion(dataIngConfig)
        dataIngArtifact = dataIngestion.initiate_data_ingestion()
        
        dataValConfig = DataValidationConfig(trainPipConfig)
        dataValidation = DataValidation(dataIngArtifact,dataValConfig)
        dataValArtifact = dataValidation.initiate_data_validation()

        dataTransConfig = DataTransformationConfig(trainPipConfig)
        dataTransformation = DataTransformation(dataValArtifact=dataValArtifact,dataTransConfig=dataTransConfig)
        dataTransArtifact = dataTransformation.initiate_data_transformation()

        modelTrainerConfig = ModelTrainerConfig(trainPipConfig)
        modelTrain = ModelTrainer(dataTransArtifact=dataTransArtifact,modelTrainerConfig=modelTrainerConfig)
        modelTrainerArtifact = modelTrain.initiate_model_trainer()


    except Exception as e:
        raise NetworkSecurityException(e,sys)



### testing with MongoDB

# import os
# from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient

# load_dotenv()
# MONGO_DB_URI = os.getenv('MONGO_DB_URI')

# try:
#     client = MongoClient(MONGO_DB_URI)
#     # Ping the server
#     client.admin.command('ping')
#     print("MongoDB is reachable!")
# except Exception as e:
#     print(f"Failed to connect to MongoDB: {e}")
