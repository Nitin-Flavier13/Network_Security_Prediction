import os,sys
import pandas as pd

from scipy.stats import ks_2samp
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file

from network_security.entity.config_entity import DataValidationConfig
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

class DataValidation:
    def __init__(self, dataIngArtifact: DataIngestionArtifact, dataValConfig: DataValidationConfig):
        try:
            self.dataIngArtifact = dataIngArtifact
            self.dataValConfig = dataValConfig
            self.schemaConfig = read_yaml_file(SCHEMA_FILE_PATH).get("columns",[])
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def check_dataset_drift(self,base_df,current_df,threshold=0.02) -> bool:
        try:
            logging.info("Started checking new Data Drift")
            status = True
            report = {}

            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)   # p-value (here the likelyhood that 2 
                                                 # of the distributions are same)
                if is_same_dist.pvalue >= threshold:
                    is_found = False
                else:
                    is_found = True 
                    status = False
                    logging.info(f"Column {col} is DRIFTED")
                report.update({
                    col: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })
                
            drift_report_file_path = self.dataValConfig.drift_report_file_path

            # creating directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,report)

            logging.info("Dataset Drift Report Uploaded Successfully")

            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_of_columns(self,dataframe: pd.DataFrame) -> bool:
        try:
            num_cols = len(self.schemaConfig)
            data_num_cols = len(dataframe.columns)
            logging.info(f"Required Number of Columns {num_cols}")
            logging.info(f"DataFrame Number of Columns {data_num_cols}")

            if num_cols == data_num_cols:
                return True
            return False

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Data Validation initiated")
            test_file_path = self.dataIngArtifact.test_file_path
            train_file_path = self.dataIngArtifact.trained_file_path

            test_dataframe = self.read_data(test_file_path)
            train_dataframe = self.read_data(train_file_path)

            logging.info("No. of columns validation Begins")

            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = "Train Data does not contains all columns"
                logging.info(error_message)

            status = status and self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = "Test Data does not contains all columns"
                logging.info(error_message)

            logging.info("No. of columns validation Done")

            status = status and self.check_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            dir_path = os.path.dirname(self.dataValConfig.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            if status:
                train_dataframe.to_csv(self.dataValConfig.valid_train_file_path,index=False,header=True)
                test_dataframe.to_csv(self.dataValConfig.valid_test_file_path,index=False,header=True)
            
            logging.info(f"Validation status: {status}")

            dataValArtifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.dataIngArtifact.trained_file_path,
                valid_test_file_path=self.dataIngArtifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.dataValConfig.drift_report_file_path
            )
            logging.info("Data Validation Completed")

            return dataValArtifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)




