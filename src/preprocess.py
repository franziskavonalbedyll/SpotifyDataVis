import pandas as pd
import os

from src.config import *
from src.utils import *


def _keep_years(df, years_to_keep) -> pd.DataFrame:
    df = df[df.date.dt.year.isin(years_to_keep)]
    return df.sort_values(by=['date'])

def _merge_charts_with_audio_features(audio_features: pd.DataFrame, years_to_keep) -> None:
    charts = pd.read_csv(CHARTS_PATH)
    charts['date'] = pd.to_datetime(charts['date'])
    charts = _keep_years(charts, years_to_keep)

    filtered_audio_features = audio_features[['url'] + AUDIO_FEATURES]

    merged_charts_df = pd.merge(charts, filtered_audio_features, on='url')

    return merged_charts_df

def _round_audio_features(df) -> pd.DataFrame:
    for audio_feature in AUDIO_FEATURES:
        df[audio_feature] = round(df[audio_feature], 2)
    return df

def _transform_dates(df) -> pd.DataFrame:
    df['year'] = df['date'].dt.year
    df['whole_date'] = df['date'].copy()
    df['date'] = df['date'].dt.strftime('%m-%d')
    return df

def _aggregate_audio_feature(df):
    df_aggregated = df.groupby(['region', 'date', 'year'], as_index=False)[AUDIO_FEATURES].mean()
    return df_aggregated

def preprocess_data(include_years: int):
    output_path = 'data/preprocessed_data/preprocessed_data.csv'
    if not os.path.exists(output_path):
        input_data = pd.read_csv(AUDIO_FEATURES_AND_GENRE_PATH)

        # Remove preprocessing steps by commenting them out
        preprocessed_df = _merge_charts_with_audio_features(input_data, include_years)
        preprocessed_df = _transform_dates(preprocessed_df)
        preprocessed_df = _aggregate_audio_feature(preprocessed_df)
        preprocessed_df = _round_audio_features(preprocessed_df)

        preprocessed_df.to_csv(output_path)


if __name__ == '__main__':
    include_years = [2019, 2020, 2021]
    preprocess_data(include_years)
