import pandas as pd
import os
import logging
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Set up logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
beginning_of_logging = datetime.datetime.now().strftime("%m.%d.%Y_%H.%M.%S")

file_handler = logging.FileHandler(f'logs/{beginning_of_logging}.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


DEV = True
CHARTS_PATH = 'charts.csv'
AUDIO_FEATURES_FILE_PATH = 'data/input_data/data_top200_top5_2019_2020_2021.csv'
PREPROCCESSED_DATA_DIR = 'data/preprocessed_data'
YEARS_OF_INTEREST = [2019, 2020, 2021]
AUDIO_FEATURES = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
               'valence', 'tempo', 'duration_ms']


def preprocess_data():
    if DEV:
        if len(os.listdir(PREPROCCESSED_DATA_DIR)) != 0:
            return

        charts = pd.read_csv(CHARTS_PATH)
        charts['date'] = pd.to_datetime(charts['date'])

        audio_features = pd.read_csv(AUDIO_FEATURES_FILE_PATH)
        filtered_audio_features = audio_features[['url'] + AUDIO_FEATURES]

        charts_dfs = {year: charts[charts.date.dt.year == year] for year in YEARS_OF_INTEREST}
        for year, df in charts_dfs.items():
            merged_charts_df = pd.merge(df, filtered_audio_features, on='url')
            merged_charts_df.to_csv(f'{PREPROCCESSED_DATA_DIR}/{year}.csv')

        logger.info('Finished preprocessing.')

def aggregate_audio_feature(df):
    df_aggregated = df.groupby(['region', 'date'], as_index=False).mean()
    return df_aggregated

def plot(df):

    valence_min = round(float(df.valence.min()), 3)
    valence_max = round(float(df.valence.max()), 3)

    fig = px.choropleth(df,
                        locations='region',
                        locationmode='country names',
                        color='valence',
                        hover_name='valence',
                        animation_frame='date',
                        projection='natural earth',
                        color_continuous_scale=px.colors.sequential.Aggrnyl,
                        range_color=(valence_min, valence_max))

    fig.update_traces(marker_line_width=0)
    fig.update_layout(showlegend=False, geo=dict(showframe=False, showcoastlines=False))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                      width=1500,
                      height=800
                      )

    last_frame_num = int(len(fig.frames) - 200)
    fig.layout['sliders'][0]['active'] = last_frame_num
    fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)

    fig.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    preprocess_data()

    fig = make_subplots(rows=1, cols=2)

    df_2019 = pd.read_csv(PREPROCCESSED_DATA_DIR + '/2019.csv')[['region', 'valence', 'date']].sort_values(by=['date'])
    df_2019['valence'] = round(df_2019['valence'], 3)
    df_2019_aggregated = aggregate_audio_feature(df_2019)

    plot_2019 = plot(df_2019_aggregated)

    plot(df_2019_aggregated)


    print("")





