import os
import sys 

from network_security.logging.logger import logging 
from network_security.exception.exception import NetworkSecurityException

from network_security.components.model_trainer import ModelTrainer
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainPipeline:
    def __init__(self):
        self.trainPipConfig = TrainingPipelineConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.dataIngConfig = DataIngestionConfig(trainPipelineConfig=self.trainPipConfig)
            dataIngestion = DataIngestion(dataIngConfig=self.dataIngConfig)
            dataIngArtifact = dataIngestion.initiate_data_ingestion()
            
            return dataIngArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
    
    def start_data_validation(self, dataIngArtifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.dataValConfig = DataValidationConfig(training_pipeline_config=self.trainPipConfig)
            dataValidation = DataValidation(
                dataIngArtifact=dataIngArtifact,
                dataValConfig=self.dataValConfig
            )
            dataValArtifact = dataValidation.initiate_data_validation()

            return dataValArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
    
    def start_data_transformation(self, dataValArtifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            self.dataTransConfig = DataTransformationConfig(trainPiplineConfig=self.trainPipConfig)
            dataTransformation = DataTransformation(
                dataValArtifact=dataValArtifact,
                dataTransConfig=self.dataTransConfig
            )
            dataTransArtifact = dataTransformation.initiate_data_transformation()

            return dataTransArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_training(self, dataTransArtifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.modelTrainerConfig = ModelTrainerConfig(trainPipelineConfig=self.trainPipConfig)
            modelTrain = ModelTrainer(
                dataTransArtifact=dataTransArtifact,
                modelTrainerConfig=self.modelTrainerConfig
            )
            modelTrainerArtifact = modelTrain.initiate_model_trainer()

            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_pipeline(self) -> ModelTrainerArtifact:
        try:
            dataIngArtifact = self.start_data_ingestion()
            dataValArtifact = self.start_data_validation(dataIngArtifact=dataIngArtifact)
            dataTransArtifact = self.start_data_transformation(dataValArtifact=dataValArtifact)
            modelTrainerArtifact = self.start_model_training(dataTransArtifact=dataTransArtifact)
            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)