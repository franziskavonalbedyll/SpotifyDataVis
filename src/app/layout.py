from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.data_loader import get_countries, AUDIO_FEATURES

countries = get_countries()
countries = countries.tolist()
countries.insert(0, 'All')

layout = html.Div(style={'height': '100vh', 'width': '100vw', 'display': 'flex', 'flexDirection': 'column'},
                  children=[
                      html.Div(className="centered-title", children="Spotify Audio Features: 2020 vs. Pre-COVID years",
                               style={'textAlign': 'center', 'fontSize': 28, 'flex': '0 1 auto'}),
                      html.Div([
                          html.Div([
                              html.Div("Select Audio Feature", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
                              dcc.Dropdown(
                                  id='audio-feature-dropdown',
                                  options=[{'label': feature.capitalize(), 'value': feature} for feature in AUDIO_FEATURES],
                                  value='valence',
                                  style={'width': '100%', 'display': 'inline-block'}
                              ),
                          ], style={'width': '30%', 'display': 'inline-block', 'paddingRight': '10px'}),
                          html.Div([
                              html.Div("Select Country for Lockdown Dates", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
                              dcc.Dropdown(
                                  id='covid-dropdown',
                                  options=[{'label': country, 'value': country} for country in countries],
                                  value='Denmark',
                                  style={'width': '100%', 'display': 'inline-block'}
                              ),
                          ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '10px'}),
                          dcc.Store(id='sort-state', data={'sorted': False})
                      ], style={'width': '75%', 'boxSizing': 'border-box',
                                'paddingTop': '25px',
                                'paddingRight': '25px',
                                'paddingLeft': '5.8%',
                                'paddingBottom': '0px',
                                'marginBottom': '0px',
                                'display': 'flex', 'alignItems': 'center'}),
                      html.Div([
                          dcc.Graph(id='heatmap', style={'height': '80vh', 'width': '100%'}),
                          dbc.Button(
                              id='sort-button',
                              children='Sort by Similarity',
                              style={'position': 'absolute', 'top': '-35px', 'right': '140px', 'fontSize': '16px'}
                          )
                      ], style={'position': 'relative', 'width': '100%', 'height': '80vh'}),
                      dbc.Modal(
                          [
                              dbc.ModalHeader(dbc.ModalTitle("Country Audio Feature Standard Deviations")),
                              dbc.ModalBody(id='modal-body'),
                              dbc.ModalFooter(
                                  dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                              ),
                          ],
                          id="modal",
                          size="lg",
                      ),
                  ])
