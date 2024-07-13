import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Beispiel-Daten automatisiert erstellen
np.random.seed(42)  # Für reproduzierbare Ergebnisse
countries = ["Belgium", "France", "Germany"]
years = ["2019", "2020", "2021"]
date_range = pd.date_range(start="2019-01-01", periods=50, freq='D')

data = []

for year in years:
    if year == "2019":
        value_range = (0.0, 0.2)
    elif year == "2020":
        value_range = (0.3, 0.5)
    elif year == "2021":
        value_range = (0.6, 0.9)

    for date in date_range:
        for country in np.random.choice(countries, size=np.random.randint(2, 4), replace=False):
            data.append({
                "date": date.strftime("%m-%d"),
                "country": country,
                "value": np.round(np.random.uniform(value_range[0], value_range[1]), 2),
                "year": year
            })

df = pd.DataFrame(data)
dates = df['date'].unique()

# Dash App initialisieren
app = dash.Dash(__name__)
app.layout = html.Div(style={'height': '100vh', 'width': '100vw'}, children=[
    html.Div([
        dcc.Dropdown(
            id='year-dropdown-1',
            options=[{'label': year, 'value': year} for year in years],
            value='2019'
        ),
        dcc.Graph(id='choropleth-map-1', style={'height': '80vh'})
    ], style={'width': '48%', 'display': 'inline-block', 'height': '80vh'}),

    html.Div([
        dcc.Dropdown(
            id='year-dropdown-2',
            options=[{'label': year, 'value': year} for year in years],
            value='2020'
        ),
        dcc.Graph(id='choropleth-map-2', style={'height': '80vh'})
    ], style={'width': '48%', 'display': 'inline-block', 'height': '80vh'}),

    html.Div([
        dcc.Slider(
            id='date-slider',
            min=0,
            max=len(dates) - 1,
            value=0,
            marks={i: dates[i] for i in range(len(dates))},
            step=1
        )
    ], style={'width': '96%', 'padding': '20px', 'margin': '0 auto'})
])


@app.callback(
    [Output('choropleth-map-1', 'figure'),
     Output('choropleth-map-2', 'figure')],
    [Input('year-dropdown-1', 'value'),
     Input('year-dropdown-2', 'value'),
     Input('date-slider', 'value')]
)
def update_maps(selected_year_1, selected_year_2, selected_date_idx):
    selected_date = dates[selected_date_idx]

    filtered_df_1 = df[(df['year'] == selected_year_1) & (df['date'] == selected_date)]
    filtered_df_2 = df[(df['year'] == selected_year_2) & (df['date'] == selected_date)]

    fig1 = px.choropleth(filtered_df_1, locations="country",
                         locationmode='country names', color="value",
                         hover_name="country", title=f"Data for {selected_year_1}-{selected_date}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         range_color=(0, 1))

    fig2 = px.choropleth(filtered_df_2, locations="country",
                         locationmode='country names', color="value",
                         hover_name="country", title=f"Data for {selected_year_2}-{selected_date}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         range_color=(0, 1))

    fig1.update_layout(coloraxis_showscale=False)

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
