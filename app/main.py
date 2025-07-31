from fastapi import FastAPI, HTTPException
from app.schemas import InferenceRequest, InferenceResponse
from app.utils import preprocess_input
from app.model import model
import numpy as np

app = FastAPI()

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    try:
        features_df = preprocess_input(request.features)
        prediction = model.predict(features_df)[0]
        probability = float(model.predict_proba(features_df)[0][1])
        return InferenceResponse(prediction=int(prediction), probability=probability)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))