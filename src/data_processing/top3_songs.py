import pandas as pd

# df_19 = pd.read_csv('data/preprocessed_data/2019.csv')
# df_20 = pd.read_csv('data/preprocessed_data/2020.csv')
# df_21 = pd.read_csv('data/preprocessed_data/2021.csv')


def _keep_european_countries(df):
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
                          'Romania', 'Slovakia',
                          'Spain', 'Sweden',
                          'Switzerland', 'Turkey',
                          'United Kingdom']

    df = df[df['region'].isin(european_countries)]

    return df

def drop_features(df):
    return df.drop(['Unnamed: 0', 'url',  'danceability', 'energy', 'loudness',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'duration_ms', 'trend', 'chart', 'streams'], axis=1)

def drop_viral50(df):
    return df[df['chart'] != 'viral50']



def get_top3_songs(dfs):
    combined_df = pd.DataFrame()
    for df in dfs:
        t_df = drop_viral50(df)
        d_df = drop_features(t_df)
        e_df = _keep_european_countries(d_df)
        
        top3_songs = e_df[e_df['rank'].isin([1, 2, 3])]
        combined_df = pd.concat([combined_df, top3_songs])



top3_songs_df = pd.read_csv('data/preprocessed_data/top3_songs.csv')

def test():
    df_pivot = pd.DataFrame(index= top3_songs_df['region'].unique() ,columns = top3_songs_df['date'].unique())
    print(df_pivot.head())
    print(df_pivot['2020-01-01'].head())

    df_pivot.at['Denmark', '2020-01-01'] = 5
    ret = df_pivot.loc['Denmark', '2020-01-01']

    for region in top3_songs_df['region'].unique():
        for date in top3_songs_df['date'].unique():
            string_d_r = "" 
            date_per_region = top3_songs_df[(top3_songs_df['region'] == region) & (top3_songs_df['date'] == date)]
            date_series = date_per_region['rank'].astype(str) + ". " + date_per_region['title'] + " - " + date_per_region['artist'] + "<br>"
            for i in date_series:
                string_d_r += i

            
            df_pivot.at[region, date] = string_d_r
        print(df_pivot.head())

    df_pivot.to_csv('data/preprocessed_data/pivot_top3_songs.csv')        
            

            
            
# test()

df_piv = pd.read_csv('data/preprocessed_data/pivot_top3_songs.csv')

cols = df_piv.columns


"""
Index(['Unnamed: 0', 'title', 'rank', 'date', 'artist', 'url', 'region',
       'chart', 'trend', 'streams', 'danceability', 'energy', 'loudness',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'duration_ms'],
      dtype='object')
"""