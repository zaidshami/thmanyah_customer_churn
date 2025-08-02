import pandas as pd
import numpy as np
import argparse
import os
from sklearn.model_selection import train_test_split

def extract_features(data):
    grouped = data.groupby('userId')
    features = pd.DataFrame(index=grouped.size().index)

    features['num_sessions'] = grouped['sessionId'].nunique()
    features['num_songs_played'] = grouped.apply(lambda x: (x['page'] == 'NextSong').sum())
    features['num_thumbs_up'] = grouped.apply(lambda x: (x['page'] == 'Thumbs Up').sum())
    features['num_thumbs_down'] = grouped.apply(lambda x: (x['page'] == 'Thumbs Down').sum())
    features['num_add_friend'] = grouped.apply(lambda x: (x['page'] == 'Add Friend').sum())
    features['avg_songs_per_session'] = features['num_songs_played'] / features['num_sessions']
    features['gender'] = grouped['gender'].first()
    features['level'] = grouped['level'].last()
    features['churn'] = grouped['churn'].max()
    features['registration_days'] = grouped.apply(lambda x: (x['ts'].max() - x['registration'].min()).days)

    return features.reset_index()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str, required=True)
    parser.add_argument('--output_data_train', type=str, required=True)
    parser.add_argument('--output_data_validation', type=str, required=True)
    args = parser.parse_args()

    # Load raw logs
    df = pd.read_json(os.path.join(args.input_data, 'log_data.json'), lines=True)

    # Filter and convert
    df = df[df['userId'].notnull() & (df['userId'] != '')]
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df['registration'] = pd.to_datetime(df['registration'], unit='ms')
    df['sessionId'] = df['sessionId'].astype(str)
    df['userId'] = df['userId'].astype(str)

    # Define churn label
    churn_users = df[df['page'] == 'Cancellation Confirmation']['userId'].unique()
    df['churn'] = df['userId'].apply(lambda x: 1 if x in churn_users else 0)

    # Extract features
    df_features = extract_features(df)

    # Encode categorical features (for XGBoost later)
    df_features['gender'] = df_features['gender'].map({'M': 0, 'F': 1})
    df_features['level'] = df_features['level'].map({'free': 0, 'paid': 1})

    # Train/test split
    train_df, val_df = train_test_split(df_features, test_size=0.2, stratify=df_features['churn'], random_state=42)

    # Save outputs
    os.makedirs(args.output_data_train, exist_ok=True)
    os.makedirs(args.output_data_validation, exist_ok=True)

    train_df.to_csv(os.path.join(args.output_data_train, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(args.output_data_validation, 'validation.csv'), index=False)

if __name__ == "__main__":
    main()