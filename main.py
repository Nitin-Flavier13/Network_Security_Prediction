import sys

from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig

if __name__ == "__main__":
    try:
        logging.info("Called the Data Ingestion Pipeline")

        trainPipConfig = TrainingPipelineConfig()
        dataIngConfig = DataIngestionConfig(trainPipConfig)
        dataIngestion = DataIngestion(dataIngConfig)
        dataIngArtifact = dataIngestion.initiate_data_ingestion()

        logging.info("Data Ingestion Pipeline Successfully executed")

        logging.info("Data Validation initiated")

        dataValConfig = DataValidationConfig(trainPipConfig)
        dataValidation = DataValidation(dataIngArtifact,dataValConfig)
        dataValArtifacts = dataValidation.initiate_data_validation()

        logging.info("Data Validation Complete")


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
