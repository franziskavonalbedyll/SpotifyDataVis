import pandas as pd
from src.config import *

def compute_audio_feature_averages(df, audio_features, countries, dates):
    results = []

    for audio_feature in audio_features:
        for country in countries:
            for date in dates:
                df_filtered = df[(df['region'] == country) & (df['date'] == date)]
                if not df_filtered.empty:
                    avg_value = round(df_filtered[audio_feature].mean(), 3)
                    results.append({
                        'region': country,
                        'audio_feature': audio_feature,
                        'date': date,
                        'all_years_avg': avg_value
                    })

    return pd.DataFrame(results)

def calculate_deviation(df, avg_df, audio_features):
    for audio_feature in audio_features:
        deviation_col = f"{audio_feature}_deviation"
        df = df.merge(
            avg_df[avg_df['audio_feature'] == audio_feature],
            on=['region', 'date'],
            how='left',
            suffixes=('', '_avg')
        )
        df[deviation_col] = round(df[audio_feature] - df['all_years_avg'], 10)
        df.drop(columns=['audio_feature', 'all_years_avg'], inplace=True)
    return df

def save_to_csv(df, path):
    df.to_csv(path, index=False)

def main():
    df = pd.read_csv(PREPROCCESSED_DATA_PATH)
    countries = df['region'].unique()
    dates = df['date'].unique()

    avg_df = compute_audio_feature_averages(df, AUDIO_FEATURES, countries, dates)
    save_to_csv(avg_df, AUDIO_FEATURES_AVGS_PATH)

    df_with_deviation = calculate_deviation(df, avg_df, AUDIO_FEATURES)
    save_to_csv(df_with_deviation, PROCESSED_DATA_PATH)

if __name__ == "__main__":
    main()
