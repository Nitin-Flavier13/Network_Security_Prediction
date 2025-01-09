import os
from datetime import datetime 

from network_security.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp = timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = training_pipeline.ARTIFACT_DIR
        self.artifact_path = os.path.join(self.artifact_dir,timestamp)


class DataIngestionConfig:
    def __init__(self,trainPipelineConfig: TrainingPipelineConfig):

        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.data_ingestion_path: str = os.path.join(
            trainPipelineConfig.artifact_path,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_path,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_file_path: str = os.path.join(
            self.data_ingestion_path,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME,
        )

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_path,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME,
        )



# artifacts-timestamp-dataingestion-featurestore-phishing.csv
# artifacts-timestamp-dataingestion-ingested-train
# artifacts-timestamp-dataingestion-ingested-test