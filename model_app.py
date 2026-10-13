import pandas as pd
import pickle
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output,MODEL_VERSION,model_is_loaded



app=FastAPI()

@app.get('/')
def home():
    return {'message':"Insurance Premium Prediction API"}

@app.get('/health')
def health_check():
    return {'status':'OK',
            'version':MODEL_VERSION,
            'model_loaded':model_is_loaded
            }


@app.post("/predict",response_model=PredictionResponse)
def predict(user_data:UserInput):

    user_input={
        'bmi':user_data.bmi,
        'age_group':user_data.age_group,
        'lifestyle_risk':user_data.lifestyle_risk,
        'city_tier':user_data.city_tier,
        'income_lpa':user_data.income_lpa,
        'occupation':user_data.occupation
    }

    try:
        prediction=predict_output(user_input)
        return JSONResponse(status_code=200,content=prediction)
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))






        
