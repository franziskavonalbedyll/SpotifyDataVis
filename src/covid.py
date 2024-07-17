import pandas as pd
from config import *

covid_df = pd.read_csv(COVID_PATH)

# print(covid_df.head())

# print(covid_df.columns[2:25:3]) # Down dates
# print(covid_df.columns[3:25:3]) # Down dates

drop_cols = covid_df.columns[1:31:3]
print(drop_cols)
covid_df.drop(columns=drop_cols)

print(covid_df.columns)

down_idx = covid_df.columns[2:25:3]
up_idx = covid_df.columns[3:25:3]

covid_df = covid_df[['Country / territory'] + list(down_idx) + list(up_idx)]

down_df = covid_df[['Country / territory'] + list(down_idx)]
up_df = covid_df[['Country / territory'] + list(up_idx)]

combined = down_df.merge(up_df, on='Country / territory')

lockdowns = combined[combined['Country / territory'] == "Australia"]

# print(lockdowns)

# print(down_df.head())
# print(up_df.head())
# print(combined.columns)

# # pick a row, then pick a column
# print(combined.iloc[6].iloc[3])


# print(covid_df[5::3])

# print(covid_df['Country / territory'].unique())