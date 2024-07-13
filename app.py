import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

from src.config import AUDIO_FEATURES


df = pd.read_csv('data/preprocessed_data/preprocessed_data.csv')[['date', 'region', 'year'] + AUDIO_FEATURES]
years = df['year'].unique()
dates = df['date'].unique()

# Liste mit Monatsnamen
month_labels = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']

# Erzeuge ein Dictionary für die Labels des Sliders
slider_marks = {i * len(dates) // 12: month for i, month in enumerate(month_labels)}

# Dash App initialisieren
app = dash.Dash(__name__)
app.layout = html.Div(style={'height': '100vh', 'width': '100vw'}, children=[
    html.Div([
        dcc.Dropdown(
            id='year-dropdown-1',
            options=[{'label': year, 'value': year} for year in years],
            value=2019  # Standardwert links auf 2019 gesetzt
        ),
        dcc.Dropdown(
            id='audio-feature-dropdown-1',
            options=[{'label': feature, 'value': feature} for feature in AUDIO_FEATURES],
            value='valence'  # Standardwert auf valence gesetzt
        ),
        dcc.Graph(id='choropleth-map-1', style={'height': '70vh'})
    ], style={'width': '48%', 'display': 'inline-block', 'height': '80vh'}),

    html.Div([
        dcc.Dropdown(
            id='year-dropdown-2',
            options=[{'label': year, 'value': year} for year in years],
            value=2020  # Standardwert rechts auf 2020 gesetzt
        ),
        dcc.Dropdown(
            id='audio-feature-dropdown-2',
            options=[{'label': feature, 'value': feature} for feature in AUDIO_FEATURES],
            value='valence'  # Standardwert auf valence gesetzt
        ),
        dcc.Graph(id='choropleth-map-2', style={'height': '70vh'})
    ], style={'width': '48%', 'display': 'inline-block', 'height': '80vh'}),

    html.Div([
        dcc.Slider(
            id='date-slider',
            min=0,
            max=len(dates) - 1,
            value=0,
            marks=slider_marks,
            step=1
        )
    ], style={'width': '96%', 'padding': '20px', 'margin': '0 auto'})
])


@app.callback(
    [Output('choropleth-map-1', 'figure'),
     Output('choropleth-map-2', 'figure')],
    [Input('year-dropdown-1', 'value'),
     Input('audio-feature-dropdown-1', 'value'),
     Input('year-dropdown-2', 'value'),
     Input('audio-feature-dropdown-2', 'value'),
     Input('date-slider', 'value')]
)
def update_maps(selected_year_1, selected_audio_feature_1, selected_year_2, selected_audio_feature_2, selected_date_idx):
    selected_date = dates[selected_date_idx]

    filtered_df_1 = df[(df['year'] == selected_year_1) & (df['date'] == selected_date)]
    filtered_df_2 = df[(df['year'] == selected_year_2) & (df['date'] == selected_date)]

    fig1 = px.choropleth(filtered_df_1, locations="region",
                         locationmode='country names', color=selected_audio_feature_1,
                         hover_name="region", title=f"Data for {selected_year_1}-{selected_date}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         range_color=(0, 1),
                         hover_data={'date': True, selected_audio_feature_1: True})

    fig2 = px.choropleth(filtered_df_2, locations="region",
                         locationmode='country names', color=selected_audio_feature_2,
                         hover_name="region", title=f"Data for {selected_year_2}-{selected_date}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         range_color=(0, 1),
                         hover_data={'date': True, selected_audio_feature_2: True})

    fig1.update_layout(coloraxis_showscale=False)

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
