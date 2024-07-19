import pandas as pd
from src.config import *

df = pd.read_csv(PROCESSED_DATA_PATH)[['date', 'region', 'year'] + DEVIATIONS_COLUMNS]
df = df[df['region'] != 'Andorra']
df = df.rename(columns={audio_feature_deviation: audio_feature for (audio_feature_deviation, audio_feature) in zip(DEVIATIONS_COLUMNS, AUDIO_FEATURES)})
years = df['year'].unique()
countries = df['region'].unique()

covid_df = pd.read_csv('data_processing/input_data/COVID-19_lockdowns_1.csv')

def get_countries():
    return countries

def get_data():
    return df

def get_covid_data():
    return covid_df

def calculate_y_bounds(df):
    bounds = {}
    for feature in AUDIO_FEATURES:
        for country in df['region'].unique():
            country_data = df[df['region'] == country]
            if not country_data.empty and feature in country_data.columns:
                ymin = country_data[feature].min()
                ymax = country_data[feature].max()
                bounds[(feature, country)] = (ymin, ymax)
            else:
                bounds[(feature, country)] = (0, 0)
    return bounds

# Calculate bounds for all audio features and countries
y_bounds = calculate_y_bounds(df)
