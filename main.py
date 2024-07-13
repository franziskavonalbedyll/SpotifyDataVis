from src.plot import plot
from src.log import get_logger
from src.preprocess import *

logger = get_logger()
DEV = True

if __name__ == '__main__':
    # Just a little working example to create a default visualization. Will be modified ...
    year_left = 2019
    year_right = 2020
    years = [year_left, year_right]
    for year in years:
        print(f"Preprocessing data for year {year}...")
        preprocess_data(year)
        print(f"Data preprocessing for year {year} complete.")

    audio_feature = 'liveness'

    df_year_left = pd.read_csv(year_to_filepath(year_left))
    df_year_left = df_year_left[['region', 'date'] + [audio_feature]]

    df_year_right = pd.read_csv(year_to_filepath(year_right))
    df_year_right = df_year_right[['region', 'date'] + [audio_feature]]

    print("Creating visualization...")
    fig = plot(df_year_left, df_year_right, audio_feature)
    print("Visualization created.")

    fig.show()
