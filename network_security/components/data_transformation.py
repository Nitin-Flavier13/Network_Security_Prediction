import os 
import sys 

import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.logging.logger import logging 
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.config_entity import DataTransformationConfig
from network_security.utils.main_utils.utils import save_numpy_array, save_obj
from network_security.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from network_security.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS 

class DataTransformation:
    def __init__(self, dataValArtifact: DataValidationArtifact, dataTransConfig: DataTransformationConfig):
        try:
            self.dataValArtifact = dataValArtifact
            self.dataTransConfig = dataTransConfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_csv(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_obj(self) -> Pipeline:
        """
        It initializes a KNN imputer object with the parameters specified in the training_pipeline.py
        and return a Pipeline object with KNNImputer as the first step

        """
        try:
            logging.info("Initializing KNN imputer obj")
            
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline([("imnputer",imputer)])

            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Data Transformation Initiated")
            train_df = self.read_csv(self.dataValArtifact.valid_train_file_path)
            test_df = self.read_csv(self.dataValArtifact.valid_test_file_path)

            # train dataframe
            ip_feature_train_df = train_df.drop([TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1,0)

            # test_dataframe
            ip_feature_test_df = test_df.drop([TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1,0)

            preprocessor = self.get_data_transformer_obj()

            trans_ip_feature_train = preprocessor.fit_transform(ip_feature_train_df)
            trans_ip_feature_test = preprocessor.transform(ip_feature_test_df)

            train_arr = np.c_[trans_ip_feature_train,np.array(target_feature_train_df)]
            test_arr = np.c_[trans_ip_feature_test,np.array(target_feature_test_df)]

            logging.info("saving transformed arrays")
            #save the files
            save_numpy_array(array=train_arr,file_path=self.dataTransConfig.transformed_train_file_path)
            save_numpy_array(array=test_arr,file_path=self.dataTransConfig.transformed_test_file_path)
            save_obj(obj=preprocessor,file_path=self.dataTransConfig.tranformed_obj_file_path)

            logging.info("Data Transformation Completed")

            # preparing artifacts
            dataTransArtifact = DataTransformationArtifact(
                transformed_train_file_path = self.dataTransConfig.transformed_train_file_path,
                transformed_test_file_path = self.dataTransConfig.transformed_test_file_path,
                transformed_object_file_path = self.dataTransConfig.tranformed_obj_file_path 
            )

            return dataTransArtifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)