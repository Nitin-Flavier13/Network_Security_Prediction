import sys

from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.exception.exception import NetworkSecurityException

if __name__ == "__main__":
    try:
        logging.info("Called the Data Ingestion Pipeline")
        trainPipConfig = TrainingPipelineConfig()
        dataIngConfig = DataIngestionConfig(trainPipConfig)
        dataIngestion = DataIngestion(dataIngConfig)
        logging.info("Data Ingestion Pipeline Successfully executed")
        artifact = dataIngestion.initiate_data_ingestion()
        print(artifact)
    except Exception as e:
        raise Exception(e,sys)



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
