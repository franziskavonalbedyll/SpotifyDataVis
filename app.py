import dash
import dash_bootstrap_components as dbc
from src.app.layout import layout
from src.app.callbacks import register_callbacks

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = layout

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
