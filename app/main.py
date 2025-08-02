from fastapi import FastAPI, HTTPException
# from app.schemas import InferenceRequest, InferenceResponse
# from app.utils import preprocess_input
# from app.model import model
import numpy as np
import subprocess
import uvicorn

import boto3
import json

from app.model import InferenceInput

app = FastAPI()

sagemaker_client = boto3.client("sagemaker-runtime", region_name="us-east-1")  # e.g., "us-east-1"

ENDPOINT_NAME = "churn-endpoint"



@app.post("/predict")
def predict(input: InferenceInput):
    try:
        features = input.instances[0]

        feature_values = [
            features["num_sessions"],
            features["num_songs_played"],
            features["num_thumbs_up"],
            features["num_thumbs_down"],
            features["num_add_friend"],
            features["avg_songs_per_session"],
            features["gender"],
            features["level"],
            features["registration_days"]
        ]

        # Convert to CSV string (no header)
        payload = ",".join(map(str, feature_values))

        response = sagemaker_client.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="text/csv",
            Body=payload
        )

        result = response["Body"].read().decode("utf-8")
        return {"prediction": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.post("/test_endpoint")
def test_endpoint():
    return {
            "status": "hi zaid 4",

        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
