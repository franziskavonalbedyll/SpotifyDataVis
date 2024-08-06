import seaborn as sns
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from utils.data_loader import get_data, get_covid_data, AUDIO_FEATURES, y_bounds, get_top3_songs_data

df = get_data()
covid_df = get_covid_data()
countries = df['region'].unique()
top3_songs_df = get_top3_songs_data()

def update_heatmap(selected_audio_feature, selected_covid, sort):
    print("Update heatmap called.")
    print(selected_audio_feature, sort)
    selected_year = 2020

    # Filter data for the selected year
    year_data = df[df['year'] == selected_year]
    year_data['date'] = year_data['year'].astype(str) + "-" + year_data['date']

    # Pivot data to have dates as columns and regions as rows
    pivot_table = year_data.pivot_table(index='region', columns='date', values=selected_audio_feature, aggfunc='mean')

    # Fill NaN values with the column mean
    pivot_table = pivot_table.apply(lambda x: x.fillna(x.mean()), axis=0)

    if sort:
        # Use seaborn's clustermap to get the sorted data with custom parameters
        clustermap = sns.clustermap(pivot_table, method='ward', metric='euclidean', cmap='RdBu', col_cluster=False)
        sorted_data = clustermap.data2d
    else:
        sorted_data = pivot_table.sort_index()

    customdata = [
        [f"Country: {country}<br>Date: {date}<br>{selected_audio_feature.capitalize()}: {value:.2f} <br>Top 3 Songs:<br>" + str(top3_songs_df.at[country, date]) for date, value in zip(sorted_data.columns, row)]
        for country, row in zip(sorted_data.index, sorted_data.values)
    ]

    # Create heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=sorted_data.values,
        x=sorted_data.columns,
        y=sorted_data.index,
        colorscale='RdBu',
        showscale=True,
        customdata=customdata,
        hovertemplate="%{customdata}<extra></extra>",
        colorbar=dict(
            title=dict(
                text="Std. Dev.",
                side="top",
                font=dict(size=17)
            ),
            tickfont=dict(size=15)  # Increase font size of colorbar numbers
        )
    ))

    # Update layout
    heatmap_fig.update_layout(
        # xaxis_title="Date",
        # yaxis_title="Country",
        yaxis=dict(
            autorange='reversed',  # Reverse the y-axis to have the countries in alphabetical order from top to bottom
            title_standoff=10,  # Add space between the y label and the axis
            tickfont=dict(size=15),  # Change font size of y-axis ticks
        ),
        xaxis=dict(
            tickmode='linear',
            ticks='outside',
            dtick='M1',
            tickfont=dict(size=15)  # Change font size of x-axis ticks
        ),
        font=dict(size=11),
        margin=dict(l=0, r=0, t=20, b=20)  # Remove margins
    )

    addLockdownAnnotations(selected_year, selected_covid, heatmap_fig)

    return heatmap_fig

def addLockdownAnnotations(selected_year, selected_covid, heatmap_fig):
    for country in countries:
        lockdowns = covid_df[covid_df['Country / territory'] == country]
        for _, lockdown in lockdowns.iterrows():
            for i in range(2, 25, 3):
                down = lockdown.iloc[i]
                up = lockdown.iloc[i + 1]
                if type(down) == str and type(up) == str:
                    if down[:4] == str(selected_year) or (up[:4] == str(selected_year) and down[:4] != str(selected_year)):
                        up_label = up
                        down_label = down
                        if up[:4] != str(selected_year): up = f"{selected_year}-12-31"
                        if down[:4] != str(selected_year): down = f"{selected_year}-01-01"
                        if country == selected_covid or selected_covid == "All":
                            # Add black line
                            heatmap_fig.add_shape(
                                type="line",
                                x0=down,
                                y0=country,
                                x1=up,
                                y1=country,
                                line=dict(color="black", width=10)
                            )
                            # Add white line for border effect
                            heatmap_fig.add_shape(
                                type="line",
                                x0=down,
                                y0=country,
                                x1=up,
                                y1=country,
                                line=dict(color="white", width=5)
                            )

def create_line_charts(selected_region, selected_audio_feature):
    filtered_df = df[df['region'] == selected_region]

    charts = []
    ymin, ymax = y_bounds.get((selected_audio_feature, selected_region), (0, 0))
    for year in range(2017, 2020 + 1):
        year_df = filtered_df[filtered_df['year'] == year]
        year_df['date'] = pd.to_datetime(year_df['date'] + '-' + year_df['year'].astype(str), format='%m-%d-%Y')

        trace = go.Scatter(
            x=year_df['date'],
            y=year_df[selected_audio_feature],
            mode='lines+markers',
            marker=dict(
                color=['blue' if val > 0 else 'red' for val in year_df[selected_audio_feature]]
            ),
            name=f'{year}'
        )

        fig = go.Figure(data=[trace])
        fig.add_trace(go.Scatter(
            x=[year_df['date'].min(), year_df['date'].max()],
            y=[0, 0],
            mode='lines',
            line=dict(dash='dash', color='green'),
            name='Mean Deviation (y=0)'
        ))

        fig.update_layout(
            title=f'{selected_audio_feature.capitalize()} Deviations in {selected_region} for {year}',
            xaxis_title='Date',
            yaxis_title='Standard Deviation',
            yaxis=dict(range=[ymin, ymax])  # Set y-axis range
        )

        charts.append(dcc.Graph(figure=fig))

    return html.Div(charts)

def toggle_modal(clickData, n_clicks, is_open, selected_audio_feature):
    if clickData:
        selected_region = clickData['points'][0]['y']
        modal_content = create_line_charts(selected_region, selected_audio_feature)
        return not is_open, modal_content
    if n_clicks:
        return not is_open, None
    return is_open, None
