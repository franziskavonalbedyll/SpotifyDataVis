from dash import Input, Output, State
from utils.plot_helpers import update_heatmap, toggle_modal

def register_callbacks(app):
    @app.callback(
        Output('sort-state', 'data'),
        [Input('sort-button', 'n_clicks')],
        [State('sort-state', 'data')]
    )
    def update_sort_state(n_clicks, sort_state):
        if n_clicks:
            sort_state['sorted'] = not sort_state['sorted']
        return sort_state

    @app.callback(
        Output('heatmap', 'figure'),
        [Input('audio-feature-dropdown', 'value'),
         Input('covid-dropdown', 'value'),
         Input('sort-state', 'data')]
    )
    def update_heatmap_callback(selected_audio_feature, selected_covid, sort_state):
        sort = sort_state['sorted']
        return update_heatmap(selected_audio_feature, selected_covid, sort)

    @app.callback(
        Output("modal", "is_open"),
        Output("modal-body", "children"),
        [Input("heatmap", "clickData"), Input("close", "n_clicks")],
        [State("modal", "is_open"),
         State('audio-feature-dropdown', 'value')]
    )
    def toggle_modal_callback(clickData, n_clicks, is_open, selected_audio_feature):
        return toggle_modal(clickData, n_clicks, is_open, selected_audio_feature)

    @app.callback(
        Output('sort-button', 'children'),
        [Input('sort-state', 'data')]
    )
    def update_button_label(sort_state):
        if sort_state['sorted']:
            return 'Sort by Country Name'
        else:
            return 'Sort by Similarity'
