import pandas as pd
from config import *

covid_df = pd.read_csv(COVID_PATH)

print(covid_df.head())

print(covid_df.columns)

print(covid_df['Country / territory'].unique())