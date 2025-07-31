import pandas as pd
import joblib
import os
from xgboost import XGBClassifier

df = pd.read_csv("features.csv")
X = df.drop(columns=['userId', 'churn'])
y = df['churn']

model = XGBClassifier(scale_pos_weight=5)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")