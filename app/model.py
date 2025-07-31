import joblib

model = joblib.load("artifacts/model.pkl")
feature_columns = joblib.load("artifacts/feature_columns.pkl")