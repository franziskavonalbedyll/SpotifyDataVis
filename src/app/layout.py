from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.data_loader import get_countries, AUDIO_FEATURES

countries = get_countries() 
countries = countries.tolist()
countries.insert(0,'All')

layout = html.Div(style={'height': '100vh', 'width': '100vw', 'display': 'flex', 'flexDirection': 'column'},
                  children=[
                      html.Div(className="centered-title", children="Average Audio Feature per Country Over Time",
                               style={'textAlign': 'center', 'fontSize': 24, 'flex': '0 1 auto'}),
                      html.Div([
                          dcc.Dropdown(
                              id='audio-feature-dropdown',
                              options=[{'label': feature.capitalize(), 'value': feature} for feature in AUDIO_FEATURES],
                              value='valence',
                              style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10px'}
                          ),
                          dcc.Dropdown(
                              id='covid-dropdown',
                              options=[{'label': country, 'value': country} for country in countries],
                              value='Denmark',
                              style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10px'}
                          ),
                          dbc.Button(
                              id='sort-button',
                              children='Sort by Similarity',
                              style={'float': 'right', 'fontSize': '16px'}
                          ),
                          dcc.Store(id='sort-state', data={'sorted': False})
                      ], style={'width': '100%', 'boxSizing': 'border-box', 
                                'padding-top': '25px', 
                                'padding-right': '25px',
                                'padding-left': '25px',
                                'padding-bottom': '0px',
                                'margin-bottom': '0px'}),
                      dcc.Graph(id='heatmap', style={'height': '80vh', 'width': '100%'}),
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
