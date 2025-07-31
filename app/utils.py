import pandas as pd
from .model import feature_columns

def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    return df[feature_columns]