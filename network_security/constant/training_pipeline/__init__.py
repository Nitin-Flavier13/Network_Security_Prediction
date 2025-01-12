import os 
import sys 

import numpy as np
import pandas as pd

columns_to_be_del = ["id","_id","index"]

# defining common constant variables for training pipeline
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkTrainPipeline"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"

TEST_FILE_NAME: str = "test.csv"
TRAIN_FILE_NAME: str = "train.csv"

### Data Ingestion realted constant
DATA_INGESTION_DATABASE_NAME: str = "NetworkDB"
DATA_INGESTION_COLLECTION_NAME: str = "PhishingWebData"

DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.3

### Data Validation related constant start with DATA_VALIDATION

SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

### Data Transformation related constants

DATA_TRANSFORMATION_DIR: str = "data_tranformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "tranformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "tranformed_object"

PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"

# knn imputer to replace nan values, it will find the 3 nearest neighbors and find the average values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}



