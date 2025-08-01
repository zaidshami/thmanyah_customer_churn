import pandas as pd
import argparse
import os
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str, required=True)
    parser.add_argument('--output_data_train', type=str, required=True)
    parser.add_argument('--output_data_validation', type=str, required=True)
    args = parser.parse_args()

    # Load and clean
    df = pd.read_json(os.path.join(args.input_data, 'log_data.json'), lines=True)
    df = df[df['userId'].notnull() & (df['userId'] != '')]
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df['registration'] = pd.to_datetime(df['registration'], unit='ms')

    # Label churn
    churn_users = df[df['page'] == 'Cancellation Confirmation']['userId'].unique()
    df['churn'] = df['userId'].apply(lambda x: 1 if x in churn_users else 0)

    # Feature engineering
    grouped = df.groupby('userId')
    features = pd.DataFrame(index=grouped.size().index)
    features['num_sessions'] = grouped['sessionId'].nunique()
    features['num_songs_played'] = grouped.apply(lambda x: (x['page'] == 'NextSong').sum())
    features['avg_songs_per_session'] = features['num_songs_played'] / features['num_sessions']
    features['churn'] = grouped['churn'].max()
    features = features.reset_index(drop=True)

    # Train/test split
    train_df, test_df = train_test_split(features, test_size=0.2, stratify=features['churn'], random_state=42)

    # Save to output directories
    os.makedirs(args.output_data_train, exist_ok=True)
    os.makedirs(args.output_data_validation, exist_ok=True)

    train_df.to_csv(os.path.join(args.output_data_train, 'train.csv'), index=False)
    test_df.to_csv(os.path.join(args.output_data_validation, 'validation.csv'), index=False)

if __name__ == "__main__":
    main()
