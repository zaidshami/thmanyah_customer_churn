from fastapi import FastAPI, HTTPException
from app.schemas import InferenceRequest, InferenceResponse
from app.utils import preprocess_input
from app.model import model
import numpy as np
import subprocess
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any
import boto3
import json


app = FastAPI()

sagemaker_client = boto3.client("sagemaker-runtime", region_name="us-east-1")  # e.g., "us-east-1"

ENDPOINT_NAME = "churn-endpoint"

class InferenceInput(BaseModel):
    instances: List[Dict[str, Any]]

@app.post("/predict")
def predict(input: InferenceInput):
    try:
        # Prepare input payload
        payload = json.dumps({"instances": input.instances})

        # Call SageMaker endpoint
        response = sagemaker_client.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",  # or "text/csv" if your model expects CSV
            Body=payload
        )

        # Parse response
        result = response["Body"].read().decode("utf-8")
        return {"prediction": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

#
#
# @app.post("/predict", response_model=InferenceResponse)
# def predict(request: InferenceRequest):
#     try:
#         features_df = preprocess_input(request.features)
#         prediction = model.predict(features_df)[0]
#         probability = float(model.predict_proba(features_df)[0][1])
#         return InferenceResponse(prediction=int(prediction), probability=probability)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@app.post("/test_endpoint")
def test_endpoint():
    return {
            "status": "hi zaid",

        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# @app.post("/rebuild-image")
# def rebuild_image():
#     try:
#         result = subprocess.run(
#             ["bash", "/home/ec2-user/deploy_churn_api.sh"],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         return {
#             "status": "success",
#             "stdout": result.stdout
#         }
#     except subprocess.CalledProcessError as e:
#         return {
#             "status": "error",
#             "stdout": e.stdout,
#             "stderr": e.stderr
#         }

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)