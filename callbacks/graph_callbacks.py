from dash import Input, Output, callback
import plotly.express as px
from data.csv_source import df
from data.constants import timestamp_options

import plotly.graph_objects as go

import json

# load building coordinates
with open('assets/buildings.json', 'r') as file:
    building_coords = json.load(file)

# function to truncate names
def truncate_name(name):
    if len(name) <= 9:
        return name
    return name[:5] + '...'

# function to convert pixels to Plotly 0-100 scale (imgs origin is top left, plotly origin is bottom left)
def normalize_pixels(x, y, img_w=791, img_h=791):
    x_norm = (x / img_w) * 100
    y_norm = (1 - (y / img_h)) * 100

    return x_norm, y_norm
 
@callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Input('location-filter', 'value'),
    Input('unit-filter', 'value'),
    Input('timestamp-filter', 'value')
)
def update_graphs(selected_locations, selected_units, selected_timestamps):

    # unpacking tuple of selected timestamp indices and mapping to corresponding dates
    start_idx, end_idx = selected_timestamps
    start_date = timestamp_options[start_idx]
    end_date = timestamp_options[end_idx]

    # filter dataframe based on filters selected
    filtered_df = df[
        (df['location'].isin(selected_locations)) & 
        (df['unit'].isin(selected_units)) &
        (df['date_only'] >= start_date) &
        (df['date_only'] <= end_date)
    ]

    # group by location and sum up value
    aggregated_df = filtered_df.groupby('location', as_index=False)['value'].sum()

    # truncate location name for display
    aggregated_df['truncated_location'] = aggregated_df['location'].apply(truncate_name)

    # plotly graph object for graph1 (heatmap)
    figure1 = go.Figure()

    # campus map
    figure1.update_layout(
        images=[dict(
            source='/assets/ssu_map_cropped.png',
            xref='x',
            yref='y',
            x=0,
            y=100,
            sizex=100,
            sizey=100,
            sizing='stretch',
            layer='below',
        )],
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False, range=[0, 100]),
        title='Map of Energy Used by Location'
    )

    # convert coordinates to scatter traces (shapes)
    building_traces = coords_to_scatter_traces(building_coords)

    # add each building to figure1
    for trace in building_traces:
        figure1.add_trace(trace)

    # plotly bar graph for graph2
    figure2 = px.bar(
        aggregated_df,
        x='value',
        y='truncated_location',
        title='Sum of Energy Consumption by Location',
        labels={'value': 'Sum of Value', 'location': 'Location'},
        template='plotly_white',
        hover_name='location'    
    )

    # plotly donut chart for graph3
    figure3 = px.pie(
        aggregated_df,
        names='truncated_location',
        values='value',
        title='Percent of Energy Used by Location',
        hole=0.5,
        hover_name='location'
    )

    # display percentage values and labels
    figure3.update_traces(textinfo='percent+label', rotation=270)

    return figure1, figure2, figure3
 
# function to convert building coordinates (json) to scatter traces (shapes with hover visuals)
def coords_to_scatter_traces(building_coords):

    building_traces = []

    for building in building_coords:
        name = building['name']

        # unpack coords (*), and pass to normalize pixels
        (x1, y1) = normalize_pixels(*building['top_left'])
        (x2, y2) = normalize_pixels(*building['bottom_right'])

        # rectange coords
        x_coords = [x1, x2, x2, x1, x1]
        y_coords = [y1, y1, y2, y2, y1]

        building_trace = go.Scatter(
        x=x_coords,
        y=y_coords,
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.25)',
        line=dict(color='blue', width=0),
        hoverinfo='text',
        text=name,
        mode='lines',
        name=name,
        )
        building_traces.append(building_trace)
        

    return building_traces

