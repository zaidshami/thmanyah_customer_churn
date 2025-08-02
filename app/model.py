# import joblib
from pydantic import BaseModel
from typing import List, Dict, Any
# model = joblib.load("artifacts/model.pkl")
# feature_columns = joblib.load("artifacts/feature_columns.pkl")


class InferenceInput(BaseModel):
    instances: List[Dict[str, Any]]