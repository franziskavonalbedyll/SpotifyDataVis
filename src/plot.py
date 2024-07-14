import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
from plotly.subplots import make_subplots

def create_choropleth(df, audio_feature, color_scale, showscale=True):
    fig = go.Choropleth(
        locations=df['region'],
        locationmode='country names',
        z=df[audio_feature],
        text=df[audio_feature],
        colorscale=color_scale,
        zmin=0,
        zmax=1,
        colorbar=dict(title=audio_feature.capitalize(), x=1.05) if showscale else None,
        marker_line_width=0,
        showscale=showscale
    )

    return fig

def create_frames(df_left, df_right, audio_feature, color_scale):
    frames = []
    dates = sorted(set(df_left['date'].unique()) | set(df_right['date'].unique()))
    for date in dates:
        frame_df_left = df_left[df_left['date'] == date]
        frame_df_right = df_right[df_right['date'] == date]
        frames.append(go.Frame(
            data=[
                create_choropleth(frame_df_left, audio_feature, color_scale),
                create_choropleth(frame_df_right, audio_feature, color_scale)
            ],
            name=date
        ))
    return frames

def create_slider(dates):
    return {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 17},
            'prefix': 'Date: ',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': -0.1,
        'steps': [{
            'args': [[date], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
            'label': date,
            'method': 'animate'
        } for date in dates]
    }

def pick_color(color_scale, val):
    idx = int(val * len(color_scale))
    return color_scale[idx]

def aggregate_audio_feature(df, audio_feature, color_scale):
    df_norm = df.copy()

    df_norm[audio_feature] = (df_norm[audio_feature] - df_norm[audio_feature].min()) / (df_norm[audio_feature].max() - df_norm[audio_feature].min())

    df_global = df_norm.groupby('date')[audio_feature].mean().reset_index()

    df_global['color'] = df.apply(lambda x: pick_color(color_scale, x[audio_feature]), axis=1)
    
    return df_global


def create_annotation(df, audio_feature, color_scale, position):
    
    df_global_audio_feature = aggregate_audio_feature(df, audio_feature, color_scale)
    
    annotations = []
    for i, date in enumerate(df_global_audio_feature['date']):
        tick_color = df_global_audio_feature.loc[df_global_audio_feature['date'] == date, 'color'].values[0]
        annotations.append(dict(
            x=(i/(len(df_global_audio_feature['date']))) * 0.89, y=position, 
            xref='paper', yref='paper',
            xanchor='left', yanchor='bottom', 
            showarrow=False, 
            font=dict(color=tick_color),
            xshift=180,
            bgcolor=tick_color,
            text='.',
            height=10, width=1,
            opacity=0.8
        ))
    return annotations

def create_play_pause_buttons():
    return {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                'label': '▶',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': '⏸',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': True,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': -0.08,
        'yanchor': 'top'
    }

def plot(df_left, df_right, audio_feature):
    color_scale = pc.sequential.Aggrnyl

    fig = make_subplots(rows=1, cols=2, subplot_titles=('2019', '2020'),
                        specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])
    print("Subplots created.")

    # Initial traces
    fig.add_trace(create_choropleth(df_left[df_left['date'] == df_left['date'].min()], audio_feature, color_scale, showscale=True), row=1, col=1)

    fig.add_trace(create_choropleth(df_right[df_right['date'] == df_right['date'].min()], audio_feature, color_scale, showscale=True), row=1, col=2)
    print("Initial traces added.")

    frames = create_frames(df_left, df_right, audio_feature, color_scale)
    print("Frames created.")

    fig.frames = frames

    slider = create_slider(sorted(set(df_left['date'].unique()) | set(df_right['date'].unique())))
    print("Slider created.")
    buttons = create_play_pause_buttons()
    print("Buttons created.")
    annotations_right = create_annotation(df_right, audio_feature, color_scale, position = -0.15)
    annotations_left = create_annotation(df_left, audio_feature, color_scale, position = -0.1)
    annotations_both = annotations_left + annotations_right
    print("Annotations created.")

    fig.update_layout(
        sliders=[slider],
        updatemenus=[buttons],
        annotations = annotations_both,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        width=1900,
        height=850
    )
    print("Layout updated.")

    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth'
    )

    # Hide the colorbar for the second choropleth trace
    fig.data[1].update(showscale=True)

    # Make the figure take up the whole window
    fig.layout.width = None
    fig.layout.height = None

    return fig



if __name__ == '__main__':
    
    data_2019 = {
        'year': 2019,
        'region': ['Germany', 'Denmark', 'Japan', 'France', 'Italy', 'Spain', 'Canada', 'Brazil', 'India', 'Australia',
                   'China', 'Russia', 'South Korea', 'Netherlands', 'Sweden', 'Norway', 'Finland', 'Mexico',
                   'Argentina', 'Chile',
                   'Germany', 'Denmark', 'Japan', 'France', 'Italy', 'Spain', 'Canada', 'Brazil', 'India', 'Australia'],
        'date': ['01-01', '01-01', '01-01', '02-01', '02-01', '02-01', '03-01', '03-01', '03-01', '04-01',
                 '04-01', '04-01', '05-01', '05-01', '05-01', '06-01', '06-01', '06-01', '07-01', '07-01',
                 '08-01', '08-01', '08-01', '09-01', '09-01', '09-01', '10-01', '10-01', '10-01', '11-01'],
        'valence': [0.3, 0.25, 0.22, 0.21, 0.18, 0.15, 0.1, 0.12, 0.14, 0.15,
                    0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35,
                    0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55]
    }

    data_2020 = {
        'year': 2020,
        'region': ['Germany', 'Denmark', 'Japan', 'France', 'Italy', 'Spain', 'Canada', 'Brazil', 'India', 'Australia',
                   'China', 'Russia', 'South Korea', 'Netherlands', 'Sweden', 'Norway', 'Finland', 'Mexico',
                   'Argentina', 'Chile',
                   'Germany', 'Denmark', 'Japan', 'France', 'Italy', 'Spain', 'Canada', 'Brazil', 'India', 'Australia'],
        'date': ['01-01', '01-01', '01-01', '02-01', '02-01', '02-01', '03-01', '03-01', '03-01', '04-01',
                 '04-01', '04-01', '05-01', '05-01', '05-01', '06-01', '06-01', '06-01', '07-01', '07-01',
                 '08-01', '08-01', '08-01', '09-01', '09-01', '09-01', '10-01', '10-01', '10-01', '11-01'],
        'valence': [0.94, 0.89, 0.85, 0.71, 0.67, 0.63, 0.81, 0.79, 0.77, 0.65,
                    0.62, 0.61, 0.75, 0.72, 0.69, 0.85, 0.82, 0.79, 0.75, 0.72,
                    0.91, 0.88, 0.84, 0.81, 0.78, 0.74, 0.9, 0.87, 0.83, 0.8]
    }


    df_left = pd.DataFrame.from_dict(data_2019)
    df_right = pd.DataFrame.from_dict(data_2020)
    audio_feature = 'valence'

    fig = plot(df_left, df_right, audio_feature)
    fig.show()
