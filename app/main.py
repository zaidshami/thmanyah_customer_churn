from fastapi import FastAPI, HTTPException
from app.schemas import InferenceRequest, InferenceResponse
from app.utils import preprocess_input
from app.model import model
import numpy as np
import subprocess

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

@app.post("/test_endpoint")
def test_endpoint():
    return {
            "status": "hi zaid",

        }


@app.post("/rebuild-image")
def rebuild_image():
    try:
        result = subprocess.run(
            ["bash", "/home/ec2-user/deploy_churn_api.sh"],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "stdout": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "stdout": e.stdout,
            "stderr": e.stderr
        }