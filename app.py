import os
import sys
import certifi
import pandas as pd
ca = certifi.where()

from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import load_obj
from network_security.pipeline.training_pipeline import TrainPipeline
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.exception.exception import NetworkSecurityException
from network_security.constant.training_pipeline import FINAL_MODEL_PATH,FINAL_PREPROCESSOR_PATH, PREDICTION_OUTPUT_PATH, OUTPUT_PREDICTION_DIR

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        modelTrainArtifact = train_pipeline.initiate_pipeline() 
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request,file: UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        best_model = load_obj(FINAL_MODEL_PATH)
        preprocessor = load_obj(FINAL_PREPROCESSOR_PATH)

        model_obj = NetworkModel(preprocessor=preprocessor,model=best_model)
        print(df.iloc[0])

        y_pred = model_obj.predict(df)
        print("Predict Output: ",y_pred)

        df['prediction'] = y_pred
        print(df['prediction'])

        os.makedirs(OUTPUT_PREDICTION_DIR,exist_ok=True)
        df.to_csv(PREDICTION_OUTPUT_PATH, index=False, header=True)

        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html",{"request": request,"table": table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)

 
if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)

# if __name__ == "__main__":
#     try:
#         train_pipeline = TrainPipeline()
#         modelTrainArtifact = train_pipeline.initiate_pipeline() 
#         print(modelTrainArtifact)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)


