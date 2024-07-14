import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.config import AUDIO_FEATURES

# Load and preprocess data
df = pd.read_csv('data/preprocessed_data/preprocessed_data.csv')[['date', 'region', 'year'] + AUDIO_FEATURES]
years = df['year'].unique()
dates = df['date'].unique()

# Map month labels to dates for slider
month_labels = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
slider_marks = {i * len(dates) // 12: month for i, month in enumerate(month_labels)}

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div(style={'height': '100vh', 'width': '100vw', 'display': 'flex', 'flexDirection': 'column'},
                      children=[
                          html.Div(className="centered-title", children="Audio Feature Analysis Over Time",
                                   style={'textAlign': 'center', 'fontSize': 24, 'flex': '0 1 auto'}),

                          html.Div([
                              html.Div([
                                  dcc.Dropdown(
                                      id='year-dropdown-1',
                                      options=[{'label': year, 'value': year} for year in years],
                                      value=2019
                                  ),
                                  dcc.Dropdown(
                                      id='audio-feature-dropdown-1',
                                      options=[{'label': feature.capitalize(), 'value': feature} for feature in
                                               AUDIO_FEATURES],
                                      value='valence'
                                  ),
                                  dcc.Graph(id='choropleth-map-1', style={'height': '50vh', 'width': '100%', 'display': 'none'})
                              ], className='half-width', style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                              html.Div([
                                  dcc.Dropdown(
                                      id='year-dropdown-2',
                                      options=[{'label': year, 'value': year} for year in years],
                                      value=2020
                                  ),
                                  dcc.Dropdown(
                                      id='audio-feature-dropdown-2',
                                      options=[{'label': feature.capitalize(), 'value': feature} for feature in
                                               AUDIO_FEATURES],
                                      value='valence'
                                  ),
                                  dcc.Graph(id='choropleth-map-2', style={'height': '50vh', 'width': '100%', 'display': 'none'})
                              ], className='half-width', style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                          ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '10px'}),

                          html.Div([
                              dcc.Graph(id='heatmap-1', style={'height': '15vh', 'margin': '0px', 'padding': '0px'}),
                              dcc.Graph(id='heatmap-2', style={'height': '15vh', 'margin': '0px', 'padding': '0px'}),
                              dcc.Slider(
                                  id='date-slider',
                                  min=0,
                                  max=len(dates) - 1,
                                  value=0,
                                  marks=slider_marks,
                                  step=1
                              )
                          ], style={'width': '100%', 'padding': '0px', 'flex': '0 1 auto'})
                      ])


@app.callback(
    [Output('choropleth-map-1', 'figure'),
     Output('choropleth-map-2', 'figure'),
     Output('heatmap-1', 'figure'),
     Output('heatmap-2', 'figure'),
     Output('choropleth-map-1', 'style'),
     Output('choropleth-map-2', 'style')],
    [Input('year-dropdown-1', 'value'),
     Input('audio-feature-dropdown-1', 'value'),
     Input('year-dropdown-2', 'value'),
     Input('audio-feature-dropdown-2', 'value'),
     Input('date-slider', 'value')]
)
def update_maps(selected_year_1, selected_audio_feature_1, selected_year_2, selected_audio_feature_2,
                selected_date_idx):
    selected_date = dates[selected_date_idx]

    # Filter data for the choropleth maps
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

    fig1.update_layout(
        title_x=0.5,
        title_y=0.94,
        coloraxis_showscale=True,
        title_font=dict(family="Circular Black", size=16),
        margin=dict(l=0, r=0, t=30, b=0),
        # gleiche Ränder
    )

    fig2.update_layout(
        title_x=0.5,
        title_y=0.94,
        title_font=dict(family="Circular Black", size=16),
        coloraxis_colorbar_title_text='',
        coloraxis_showscale=True,
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Filter and aggregate data for heatmaps
    heatmap_data_1 = df[df['year'] == selected_year_1]
    heatmap_data_2 = df[df['year'] == selected_year_2]

    # Append year to date to form datetime
    heatmap_data_1['datetime'] = pd.to_datetime(heatmap_data_1['year'].astype(str) + '-' + heatmap_data_1['date'], format='%Y-%m-%d')
    heatmap_data_2['datetime'] = pd.to_datetime(heatmap_data_2['year'].astype(str) + '-' + heatmap_data_2['date'], format='%Y-%m-%d')

    heatmap_data_1 = heatmap_data_1.groupby('datetime')[selected_audio_feature_1].mean().reset_index()
    heatmap_data_2 = heatmap_data_2.groupby('datetime')[selected_audio_feature_2].mean().reset_index()

    heatmap_fig_1 = go.Figure(data=go.Heatmap(
        z=heatmap_data_1[selected_audio_feature_1],
        x=heatmap_data_1['datetime'],
        y=[selected_audio_feature_1] * len(heatmap_data_1),  # y-axis to display the audio feature name
        colorscale='Viridis',
        showscale=False,  # Remove colorscale
        zmin=0, zmax=1
    ))
    heatmap_fig_1.add_vline(x=heatmap_data_1['datetime'].iloc[selected_date_idx], line_width=3, line_dash="dash", line_color="red")
    heatmap_fig_1.update_layout(
        xaxis=dict(
            title='Date',
        ),
        yaxis=dict(visible=False)  # Hide y-axis
    )

    heatmap_fig_2 = go.Figure(data=go.Heatmap(
        z=heatmap_data_2[selected_audio_feature_2],
        x=heatmap_data_2['datetime'],
        y=[selected_audio_feature_2] * len(heatmap_data_2),  # y-axis to display the audio feature name
        colorscale='Viridis',
        showscale=False,  # Remove colorscale
        zmin=0, zmax=1
    ))
    heatmap_fig_2.add_vline(x=heatmap_data_2['datetime'].iloc[selected_date_idx], line_width=3, line_dash="dash", line_color="red")
    heatmap_fig_2.update_layout(
        xaxis=dict(
            title='Date',
        ),
        yaxis=dict(visible=False)  # Hide y-axis
    )

    return fig1, fig2, heatmap_fig_1, heatmap_fig_2, {'height': '50vh', 'width': '100%', 'display': 'block'}, {'height': '50vh', 'width': '100%', 'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)
