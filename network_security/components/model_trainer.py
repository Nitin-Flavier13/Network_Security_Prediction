import os 
import sys 
import mlflow
import dagshub

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

from network_security.logging.logger import logging
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.constant.training_pipeline import FINAL_MODEL_PATH, FINAL_PREPROCESSOR_PATH, FINAL_MODEL_DIR
from network_security.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact, ClassificationMetricArtifact

from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from network_security.utils.main_utils.utils import save_obj, load_obj, load_numpy_array_data, evaluate_models


dagshub.init(repo_owner='nitinflavier13', repo_name='Network_Security_Prediction', mlflow=True)
class ModelTrainer:
    def __init__(self, dataTransArtifact: DataTransformationArtifact, modelTrainerConfig: ModelTrainerConfig):
        try:    
            self.dataTransArtifact = dataTransArtifact
            self.modelTrainerConfig = modelTrainerConfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model_name,best_model,classificationMetric: ClassificationMetricArtifact) -> None:
        try:
            with mlflow.start_run(run_name=f"{best_model_name}_best_model"):
                f1_score = classificationMetric.f1_score
                recall_score = classificationMetric.recall_score
                precision_score = classificationMetric.precision_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.log_metric("precision_score",precision_score)

                mlflow.sklearn.log_model(best_model,"model")

        except Exception as e:
            NetworkSecurityException(e,sys)
    
    def train_model(self,x_train, y_train, x_test, y_test) -> ModelTrainerArtifact:
        try:    
            models = {
                "RandomForest": RandomForestClassifier(verbose=1),
                "DecisionTree": DecisionTreeClassifier(),
                "GradientBoosting": GradientBoostingClassifier(verbose=1),
                "LogisticRegression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }
            params = {
                "DecisionTree": {
                    'criterion': ['gini','entropy','log_loss'],
                    # 'splitter': ['best','random'],
                    # 'max_features': ['sqrt','log2']
                },
                "RandomForest": {
                    # 'criterion': ['gini','entropy','log_loss'],
                    # 'max_features': ['sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "GradientBoosting": {
                    # 'loss': ['log_loss','exponential'],
                    'learning_rate': [0.1,0.01,0.05,0.001],
                    'subsample': [0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion': ['squared_error','friedman_mse'],
                    # 'max_features': ['sqrt','log2','auto'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LogisticRegression": {
                    "solver": ['liblinear','saga'],
                    "penalty": ['l1']
                },
                "AdaBoost": {
                    "learning_rate": [0.1,0.01,0.5,0.001],
                    "n_estimators": [8,16,32,64,128,256]
                }
            }
            logging.info("Hyper Parameter Tuning started")
            model_report:dict = evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)

            best_model_name = max(model_report,key=lambda x:model_report[x][1])
            best_model = model_report[best_model_name][0]
            best_score = model_report[best_model_name][1]

            logging.info(f"The best model is {best_model_name} with score of {best_score}")

            y_pred_train = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_pred_train)

            y_pred_test = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_pred_test)

            # track the mlflow
            self.track_mlflow(best_model_name,best_model,classification_train_metric)
            self.track_mlflow(best_model_name,best_model,classification_test_metric)

            preprocessor = load_obj(file_path=self.dataTransArtifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.modelTrainerConfig.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            networkModel = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_obj(file_path=self.modelTrainerConfig.trained_model_file_path,obj=networkModel)
            
            logging.info(f"Saved Trained Model to {self.modelTrainerConfig.trained_model_file_path}")

            modelTrainerArtifact = ModelTrainerArtifact(
                trained_model_file_path=self.modelTrainerConfig.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            os.makedirs(FINAL_MODEL_DIR,exist_ok=True)
            logging.info("Saving Model and preprocessing file")
            save_obj(FINAL_MODEL_PATH,best_model)
            save_obj(FINAL_PREPROCESSOR_PATH,preprocessor)

            return modelTrainerArtifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:  
            logging.info("Model Training Initiated")
            test_file_path = self.dataTransArtifact.transformed_test_file_path
            train_file_path = self.dataTransArtifact.transformed_train_file_path

            # load trained and test data
            test_arr = load_numpy_array_data(test_file_path)
            train_arr = load_numpy_array_data(train_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            modelTrainerArtifact = self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)

            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


