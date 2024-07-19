import pandas as pd
from src.config import *


def compute_audio_feature_statistics(df, audio_features, countries, dates):
    results = []

    for audio_feature in audio_features:
        for country in countries:
            for date in dates:
                df_filtered = df[(df['region'] == country) & (df['date'] == date)]
                if not df_filtered.empty:
                    avg_value = round(df_filtered[audio_feature].mean(), 3)
                    std_value = round(df_filtered[audio_feature].std(), 3)
                    results.append({
                        'region': country,
                        'audio_feature': audio_feature,
                        'date': date,
                        'all_years_avg': avg_value,
                        'all_years_std': std_value
                    })

    return pd.DataFrame(results)


def calculate_deviation(df, stats_df, audio_features):
    for audio_feature in audio_features:
        abs_deviation_col = f"{audio_feature}_deviation"
        std_deviation_col = f"{audio_feature}_std_deviation"

        df = df.merge(
            stats_df[stats_df['audio_feature'] == audio_feature],
            on=['region', 'date'],
            how='left',
            suffixes=('', '_stats')
        )

        df[abs_deviation_col] = round(df[audio_feature] - df['all_years_avg'], 10)
        df[std_deviation_col] = round((df[audio_feature] - df['all_years_avg']) / df['all_years_std'], 10)

        df.drop(columns=['audio_feature', 'all_years_avg', 'all_years_std'], inplace=True)

    return df


def save_to_csv(df, path):
    df.to_csv(path, index=False)


def main():
    df = pd.read_csv(PREPROCCESSED_DATA_PATH)
    countries = df['region'].unique()
    dates = df['date'].unique()

    stats_df = compute_audio_feature_statistics(df, AUDIO_FEATURES, countries, dates)
    save_to_csv(stats_df, AUDIO_FEATURES_AVGS_PATH)

    df_with_deviation = calculate_deviation(df, stats_df, AUDIO_FEATURES)
    save_to_csv(df_with_deviation, PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()
