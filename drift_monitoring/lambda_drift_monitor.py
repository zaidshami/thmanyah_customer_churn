# import boto3
# import pandas as pd
# from scipy.stats import ks_2samp
# from sklearn.metrics import f1_score
# import json
#
# def lambda_handler(event, context):
#     s3 = boto3.client('s3')
#
#     ref_df = pd.read_csv("s3://my-bucket/drift/reference_distribution.csv")
#     recent_df = pd.read_csv("s3://my-bucket/drift/recent_inference_data.csv")
#
#     drift_report = {}
#     for col in ref_df.columns:
#         stat, p_value = ks_2samp(ref_df[col], recent_df[col])
#         drift_report[col] = {'p_value': p_value, 'drift_detected': p_value < 0.1}
#
#     try:
#         preds = pd.read_csv("s3://my-bucket/drift/recent_predictions.csv")
#         new_f1 = f1_score(preds['true'], preds['pred'])
#         concept_drift = new_f1 < 0.75
#     except:
#         new_f1 = None
#         concept_drift = False
#
#     if any([v['drift_detected'] for v in drift_report.values()]) or concept_drift:
#         sns = boto3.client('sns')
#         sns.publish(
#             TopicArn='arn:aws:sns:region:account-id:ChurnModelNotifications',
#             Subject='⚠️ Drift Detected',
#             Message='Data or concept drift has been detected in the churn model.'
#         )
#
#     return {"status": "completed"}
