# evaluate.py

import subprocess
# subprocess.check_call(["pip", "install", "xgboost", "scikit-learn", "--quiet"])
subprocess.check_call(["pip", "install", "--quiet", "xgboost==1.7.6", "pandas==1.5.3", "scikit-learn==1.2.2", "numpy==1.23.5"])

import argparse
import os
import json
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import tarfile



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, required=True)
    parser.add_argument('--test_data', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    args = parser.parse_args()

    model_tar_path = os.path.join(args.model_dir, "model.tar.gz")
    if os.path.exists(model_tar_path):
        with tarfile.open(model_tar_path) as tar:
            tar.extractall(path=args.model_dir)

    # Load model
    model = xgb.Booster()
    model.load_model(os.path.join(args.model_dir, "xgboost-model.json"))

    # Load test data
    df = pd.read_csv(os.path.join(args.test_data, 'validation.csv'))
    X = df.drop(columns=["churn"])
    y = df["churn"]

    dval = xgb.DMatrix(X)
    preds = model.predict(dval)

    auc = roc_auc_score(y, preds)
    print(f"Evaluation AUC: {auc:.4f}")

    # Output metrics for SageMaker pipeline
    os.makedirs(args.output_dir, exist_ok=True)
    metrics = {
        "metrics": {
            "auc": auc
        }
    }

    with open(os.path.join(args.output_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    main()
