import pandas as pd
from datetime import datetime
from src.config import CHARTS_PATH, european_countries

# Load the data_processing
data = pd.read_csv(CHARTS_PATH)

# Adjusting the example data_processing for date parsing
data['date'] = pd.to_datetime(data['date'])

# Filter data_processing for the year 2020
data_2020 = data[data['date'].dt.year == 2020]

# Filter data_processing for the specified European countries
data_european = data_2020[data_2020['region'].isin(european_countries)]

# Count title frequency per date and keep only the top 10 per date
top_songs_per_date = data_european.groupby(['date', 'title']).size().reset_index(name='frequency')
top_songs_per_date = top_songs_per_date.sort_values(['date', 'frequency'], ascending=[True, False])

# Get the top 10 songs per date
top_10_songs = top_songs_per_date.groupby('date').head(10)

# Create a DataFrame for the desired format
result_list = []
for date, group in top_10_songs.groupby('date'):
    top_songs = group.sort_values(by='frequency', ascending=False).head(10)
    for rank, (index, row) in enumerate(top_songs.iterrows(), start=1):
        result_list.append({'date': date, 'rank': rank, 'title': row['title'], 'frequency': row['frequency']})

result_df = pd.DataFrame(result_list)
result_df.to_csv('top10.csv')
