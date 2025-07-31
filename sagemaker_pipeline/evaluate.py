import pandas as pd
import joblib
from sklearn.metrics import classification_report, f1_score
import json

df = pd.read_csv("features.csv")
X = df.drop(columns=['userId', 'churn'])
y = df['churn']

model = joblib.load("model.pkl")
y_pred = model.predict(X)

report = classification_report(y, y_pred, output_dict=True)
f1 = f1_score(y, y_pred)

with open("evaluation.json", "w") as f:
    json.dump({"f1_score": f1}, f)