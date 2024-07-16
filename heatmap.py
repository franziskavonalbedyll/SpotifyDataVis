import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

from src.config import AUDIO_FEATURES

# Load and preprocess data
df = pd.read_csv('data/preprocessed_data/preprocessed_data.csv')[['date', 'region', 'year'] + AUDIO_FEATURES]
years = df['year'].unique()
#dates = pd.date_range(start='1/1/2019', end='12/31/2019', freq='D').strftime('%m-%d')  # Generate a list of dates from Jan 1 to Dec 31
countries = df['region'].unique()

covid_df = pd.read_csv('data/input_data/COVID-19_lockdowns_1.csv')

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
                                  value=2020,
                                  style={'width': '45%', 'display': 'inline-block'}
                              ),
                              dcc.Dropdown(
                                  id='audio-feature-dropdown',
                                  options=[{'label': feature.capitalize(), 'value': feature} for feature in AUDIO_FEATURES],
                                  value='valence',
                                  style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10px'}
                              ),
                          ], style={'width': '100%', 'padding': '20px', 'boxSizing': 'border-box'}),
                          html.Div([
                              dcc.Dropdown(
                                  id='covid-dropdown',
                                  options=[{'label': country, 'value': country} for country in countries],
                                  value='Denmark',
                                  style={'width': '45%'}
                              )
                          ],style={'width': '100%', 'padding': '20px', 'boxSizing': 'border-box'}),
                          dcc.Graph(id='heatmap', style={'height': '80vh', 'width': '100%'})
                      ])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('audio-feature-dropdown', 'value'),
     Input('covid-dropdown', 'value')]
)


def update_heatmap(selected_year, selected_audio_feature, selected_covid):
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
        hovertemplate="%{customdata}<extra></extra>",
    ))

    # Define month labels
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tickvals = [f"{month:02d}-01" for month in range(1, 13)]

                        
    # Update layout
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
    addLockdownAnnotations(selected_year, selected_covid, heatmap_fig)

    return heatmap_fig

def addLockdownAnnotations(selected_year, selected_covid, heatmap_fig):
    for country in countries:         
        lockdowns = covid_df[covid_df['Country / territory'] == country]
        for _, lockdown in lockdowns.iterrows():
            down = lockdown['First lockdown']
            up = lockdown['First lockdown.1']
            if type(down) == str and type(up) == str:
                if down[:4] == str(selected_year) or (up[:4] == str(selected_year) and down[:4] != str(selected_year)):
                    if up[:4] != str(selected_year): up = f"{selected_year}-12-31"
                    if down[:4] != str(selected_year): down = f"{selected_year}-01-01"
                    if country == selected_covid:
                        heatmap_fig.add_annotation(x=down, y=country, text=down, bgcolor="red", arrowcolor="red", showarrow=True, arrowhead=1, opacity=0.9)
                        heatmap_fig.add_annotation(x=up, y=country, text=up, bgcolor="orange", arrowcolor="orange", showarrow=True, arrowhead=1, opacity=0.9)

                    heatmap_fig.add_trace(go.Scatter(x=[down, up], y=[country, country], mode="lines", line=dict(color="red", width=1.5), showlegend=False, opacity=0.8))

if __name__ == '__main__':
    app.run_server(debug=True)
