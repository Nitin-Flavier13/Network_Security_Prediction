import yaml
import mlflow
import pickle
import os,sys 

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path: str,content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        
        with open(file_path,"w") as file:
            yaml.dump(content,file)

    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_numpy_array(file_path: str,array: np.array) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_obj(file_path: str,obj: object) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_obj(file_path: str):
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file path does not exists {file_path}",sys)
        
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array_data(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}
        for model_name, model in models.items():
            param = params.get(model_name,{})

            with mlflow.start_run(run_name=f"{model_name}_hyperparam_tuning", nested=True):
                gs = GridSearchCV(estimator=model,param_grid=param,cv=3)
                gs.fit(x_train,y_train)

                # Log the best params
                mlflow.log_params(gs.best_params_)

                model.set_params(**gs.best_params_)
                model.fit(x_train,y_train)

                y_test_pred = model.predict(x_test)
                y_train_pred = model.predict(x_train)

                train_model_score = accuracy_score(y_train,y_train_pred)
                test_model_score = accuracy_score(y_test,y_test_pred)

                # Log the accuracy scores
                mlflow.log_metric("train_accuracy", train_model_score)
                mlflow.log_metric("test_accuracy", test_model_score)

                # Log the model
                mlflow.sklearn.log_model(model, f"{model_name}_model")

                report[model_name] = [model,test_model_score]

        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)