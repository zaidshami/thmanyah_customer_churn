import pandas as pd
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str, required=True)
    parser.add_argument('--output_data', type=str, required=True)
    args = parser.parse_args()

    df = pd.read_json(os.path.join(args.input_data, 'log_data.json'), lines=True)
    df = df[df['userId'].notnull() & (df['userId'] != '')]
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df['registration'] = pd.to_datetime(df['registration'], unit='ms')

    churn_users = df[df['page'] == 'Cancellation Confirmation']['userId'].unique()
    df['churn'] = df['userId'].apply(lambda x: 1 if x in churn_users else 0)

    grouped = df.groupby('userId')
    features = pd.DataFrame(index=grouped.size().index)
    features['num_sessions'] = grouped['sessionId'].nunique()
    features['num_songs_played'] = grouped.apply(lambda x: (x['page'] == 'NextSong').sum())
    features['avg_songs_per_session'] = features['num_songs_played'] / features['num_sessions']
    features['churn'] = grouped['churn'].max()
    features = features.reset_index()

    features.to_csv(os.path.join(args.output_data, 'features.csv'), index=False)

if __name__ == "__main__":
    main()