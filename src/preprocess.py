import pandas as pd
import os

from src.config import *
from src.utils import *


def _create_df_per_year(df, year) -> pd.DataFrame:
    df_per_year = df[df.date.dt.year == year]
    return df_per_year.sort_values(by=['date'])

def _merge_charts_with_audio_features(audio_features: pd.DataFrame, year) -> None:
    charts = pd.read_csv(CHARTS_PATH)
    charts['date'] = pd.to_datetime(charts['date'])
    charts = _create_df_per_year(charts, year)

    filtered_audio_features = audio_features[['url'] + AUDIO_FEATURES]

    merged_charts_df = pd.merge(charts, filtered_audio_features, on='url')

    return merged_charts_df

def _round_audio_features(df) -> pd.DataFrame:
    for audio_feature in AUDIO_FEATURES:
        df[audio_feature] = round(df[audio_feature], 2)
    return df

def _transform_dates(df) -> pd.DataFrame:
    df['date'] = df['date'].dt.strftime('%d-%m')
    return df

def _aggregate_audio_feature(df):
    df_aggregated = df.groupby(['region', 'date'], as_index=False)[AUDIO_FEATURES].mean()
    return df_aggregated

def preprocess_data(year: int):
    output_path = year_to_filepath(year)
    if not os.path.exists(output_path):
        input_data = pd.read_csv(AUDIO_FEATURES_AND_GENRE_PATH)

        # Remove preprocessing steps by commenting them out
        preprocessed_df = _merge_charts_with_audio_features(input_data, year)
        preprocessed_df = _create_df_per_year(preprocessed_df, year)
        preprocessed_df = _transform_dates(preprocessed_df)
        preprocessed_df = _aggregate_audio_feature(preprocessed_df)
        preprocessed_df = _round_audio_features(preprocessed_df)

        preprocessed_df.to_csv(output_path)


if __name__ == '__main__':
    preprocess_data(2019)
