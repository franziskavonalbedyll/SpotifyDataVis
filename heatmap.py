import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

from src.config import AUDIO_FEATURES

# Load and preprocess data
df = pd.read_csv('data/preprocessed_data/preprocessed_data.csv')[['date', 'region', 'year'] + AUDIO_FEATURES]
years = df['year'].unique()

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div(style={'height': '100vh', 'width': '100vw', 'display': 'flex', 'flexDirection': 'column'},
                      children=[
                          html.Div(className="centered-title", children="Average Audio Feature per Country Over Time",
                                   style={'textAlign': 'center', 'fontSize': 24, 'flex': '0 1 auto'}),
                          html.Div([
                              dcc.Dropdown(
                                  id='year-dropdown',
                                  options=[{'label': year, 'value': year} for year in years],
                                  value=2019,
                                  style={'width': '45%', 'display': 'inline-block'}
                              ),
                              dcc.Dropdown(
                                  id='audio-feature-dropdown',
                                  options=[{'label': feature.capitalize(), 'value': feature} for feature in AUDIO_FEATURES],
                                  value='valence',
                                  style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10px'}
                              )
                          ], style={'width': '100%', 'padding': '20px', 'boxSizing': 'border-box'}),
                          dcc.Graph(id='heatmap', style={'height': '80vh', 'width': '100%'})
                      ])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('audio-feature-dropdown', 'value')]
)
def update_heatmap(selected_year, selected_audio_feature):
    # Filter data for the selected year
    year_data = df[df['year'] == selected_year]
    year_data['date'] = year_data['year'].astype(str) + "-" + year_data['date']

    # Pivot data to have dates as columns and regions as rows
    pivot_table = year_data.pivot_table(index='region', columns='date', values=selected_audio_feature, aggfunc='mean')

    # Prepare customdata for hover labels
    customdata = [
        [f"Country: {country}<br>Date: {date}<br>{selected_audio_feature.capitalize()}: {value:.2f}"
         for date, value in zip(pivot_table.columns, row)]
        for country, row in zip(pivot_table.index, pivot_table.values)
    ]

    # Create heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Viridis',
        showscale=True,
        customdata=customdata,
        hovertemplate="%{customdata}<extra></extra>"
    ))

    # Define month labels
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tickvals = [f"{month:02d}-01" for month in range(1, 13)]

    heatmap_fig.update_layout(
        title=f"Average {selected_audio_feature.capitalize()} per Country in {selected_year}",
        xaxis_title="Date",
        yaxis_title="Country",
        yaxis=dict(autorange='reversed'),  # Reverse the y-axis to have the countries in alphabetical order from top to bottom
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=month_labels
        )
    )

    return heatmap_fig

if __name__ == '__main__':
    app.run_server(debug=True)
