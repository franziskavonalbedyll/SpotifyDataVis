AUDIO_FEATURES_AND_GENRE_PATH = 'data_processing/input_data/data_europe_top200_2017_2018_2019_2020_2021.csv'
PREPROCCESSED_DATA_PATH = 'data_processing/preprocessed_data/preprocessed_data.csv'
CHARTS_PATH = 'data_processing/input_data/charts.csv'
COVID_PATH = 'data_processing/input_data/COVID-19_lockdowns_1.csv'
AUDIO_FEATURES_AVGS_PATH = 'data_processing/preprocessed_data/audio_features_avg.csv'
PROCESSED_DATA_PATH = 'data_processing/preprocessed_data/processed_data.csv'

PRE_COVID_YEARS = [2017, 2018, 2019]
AUDIO_FEATURES = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
DEVIATIONS_COLUMNS = [f"{audio_feature}_deviation" for audio_feature in AUDIO_FEATURES]
european_countries = ['Andorra', 'Austria',
                      'Belgium', 'Bulgaria',
                      'Czech Republic', 'Denmark',
                      'Estonia', 'Finland',
                      'France', 'Germany',
                      'Greece', 'Hungary',
                      'Iceland', 'Ireland',
                      'Italy', 'Latvia',
                      'Lithuania', 'Luxembourg',
                      'Netherlands', 'Norway',
                      'Poland', 'Portugal',
                      'Romania', 'Russia',
                      'Slovakia', 'Spain',
                      'Sweden', 'Switzerland',
                      'Turkey', 'Ukraine',
                      'United Kingdom']