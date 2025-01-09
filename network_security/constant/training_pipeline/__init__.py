import os 
import sys 

import numpy as np
import pandas as pd

# defining common constant variables for training pipeline

TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkTrainPipeline"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"

TEST_FILE_NAME: str = "test.csv"
TRAIN_FILE_NAME: str = "train.csv"

### Data Ingestion realted constant

DATA_INGESTION_DATABASE_NAME: str = "NetworkDB"
DATA_INGESTION_COLLECTION_NAME: str = "PhishingData"

DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.3