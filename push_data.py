import os
import sys
import json 
import certifi

import numpy as np
import pandas as pd

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")

# certificate authorities, makes sure the server we are connected to is trusted
ca = certifi.where()

class NetworkDataETL():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json(self,file_path):
        try:
            logging.info("initiated csv to json")

            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            logging.info("completed transformation from csv to json")

            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def load_data_tomongo(self,records,database,collection) -> int:
        try:
            logging.info("initiated loading data to MongoDb")
            self.database = database
            self.records = records
            self.collection = collection 

            self.mongoClient = MongoClient(MONGO_DB_URI)

            self.database = self.mongoClient[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            logging.info("loaded data to MongoDB")
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    etl_obj = NetworkDataETL()
    records = etl_obj.csv_to_json(file_path=DATA_FILE_PATH)
    no_of_records = etl_obj.load_data_tomongo(records=records,database=DATABASE,collection=COLLECTION)
    print(no_of_records)
