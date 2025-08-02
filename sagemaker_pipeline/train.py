import argparse
import os
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, required=True)
    parser.add_argument('--validation', type=str, required=True)
    parser.add_argument('--model_dir', type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()

    # Load datasets
    train_df = pd.read_csv(os.path.join(args.train, 'train.csv'))
    val_df = pd.read_csv(os.path.join(args.validation, 'validation.csv'))

    X_train = train_df.drop(columns=["churn"])
    y_train = train_df["churn"]
    X_val = val_df.drop(columns=["churn"])
    y_val = val_df["churn"]

    # Convert to DMatrix
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)

    # XGBoost training
    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "verbosity": 1
    }

    model = xgb.train(params, dtrain, evals=[(dval, "validation")])

    # Predict for evaluation
    val_preds = model.predict(dval)
    auc = roc_auc_score(y_val, val_preds)

    print(f"AUC on validation set: {auc:.4f}")

    # Save the model
    os.makedirs(args.model_dir, exist_ok=True)
    model.save_model(os.path.join(args.model_dir, "xgboost-model.json"))

if __name__ == "__main__":
    main()