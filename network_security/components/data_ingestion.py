import os
import sys 

import pymongo
import numpy as np
import pandas as pd

from typing import List
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split

from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataIngestionArtifact

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self,dataIngConfig: DataIngestionConfig):
        try:
            self.dataIngConfig = dataIngConfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            database_name = self.dataIngConfig.database_name
            collection_name = self.dataIngConfig.collection_name

            self.mongoClient = MongoClient(MONGO_DB_URI)
            collection = self.mongoClient[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(["_id"],axis=1,inplace=True)

            df.replace({"na":np.nan},inplace=True)

            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_path = self.dataIngConfig.feature_store_file_path

            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_path,index=False,header=True)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_train_test_data(self, dataframe: pd.DataFrame):
        try:
            train_data, test_data = train_test_split(
                dataframe,
                test_size=self.dataIngConfig.train_test_split_ratio
            )

            dir_path = os.path.dirname(self.dataIngConfig.training_file_path)
            os.makedirs(dir_path)

            train_data.to_csv(self.dataIngConfig.training_file_path,index=False,header=True)
            test_data.to_csv(self.dataIngConfig.testing_file_path,index=False,header=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Data Ingestion initiated")
            dataframe = self.export_collection_as_dataframe()

            logging.info("Storing dataframe into features folder")
            self.export_data_into_feature_store(dataframe=dataframe)

            logging.info("Initiated Train Test Split")
            self.split_train_test_data(dataframe)

            dataIngArtifact = DataIngestionArtifact(
                trained_file_path = self.dataIngConfig.training_file_path,
                test_file_path = self.dataIngConfig.testing_file_path
            )

            logging.info("Data Ingestion Steps Completed")

            return dataIngArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


