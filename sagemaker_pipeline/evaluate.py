# evaluate.py

import subprocess
# subprocess.check_call(["pip", "install", "xgboost", "scikit-learn", "--quiet"])
subprocess.check_call(["pip", "install", "--quiet", "--no-warn-conflicts", "xgboost==1.7.6", "pandas==1.5.3",
                       "scikit-learn==1.2.2", "numpy==1.23.5"])

import argparse
import os
import json
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import tarfile
from sklearn.metrics import recall_score



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
    preds_proba = model.predict(dval)



    # Convert probabilities to binary predictions
    preds_binary = [1 if p >= 0.5 else 0 for p in preds_proba]

    # Calculate recall
    recall = recall_score(y, preds_binary)
    print(f"validation:recall={recall:.4f}")  # ✅ for SageMaker metric parsing

    # Output metrics for SageMaker pipeline
    os.makedirs(args.output_dir, exist_ok=True)
    metrics = {
        "metrics": {
            "recall": recall
        }
    }
    # auc = roc_auc_score(y, preds)
    # print(f"Evaluation AUC: {auc:.4f}")
    #
    # # Output metrics for SageMaker pipeline
    # os.makedirs(args.output_dir, exist_ok=True)
    # metrics = {
    #     "metrics": {
    #         "auc": auc
    #     }
    # }

    with open(os.path.join(args.output_dir, "evaluation.json"), "w") as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    main()
