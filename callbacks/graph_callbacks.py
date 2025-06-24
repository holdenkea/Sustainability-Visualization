from dash import Input, Output, callback
import plotly.express as px
from data.csv_source import df
from data.constants import timestamp_options
import plotly.graph_objects as go

import json

# function to truncate names
def truncate_name(name):
    if "Green Music Center".lower() in name.lower():
        return "Green Music Center"
    elif "Ives Hall".lower() in name.lower():
        return "Ives Hall"
    elif "Nichols Hall".lower() in name.lower():
        return "Nichols Hall"
    elif "Physical Education".lower() in name.lower():
        return "Physical Education"
    elif "Rachel Carson Hall".lower() in name.lower():
        return "Rachel Carson Hall"
    elif "Student Health Center".lower() in name.lower():
        return "Student Health Center"
    elif "Student Center".lower() in name.lower():
        return "Student Center"
    elif "Wine Spectator Learning".lower() in name.lower():
        return "Wine Spectator Center"
    else:
        return None
 
# callback which updates the graphs when any of the input ids are changed 
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

    # code for debugging contents of aggregated_df
    aggregated_df.to_csv('temp_agg_df.csv', index=False)

    # update map (plotly graph objects with MapLibre map)
    figure1 = update_figure1(aggregated_df)

    # update plotly bar graph 
    figure2 = update_figure2(aggregated_df)

    # update plotly donut chart 
    figure3 = update_figure3(aggregated_df)

    return figure1, figure2, figure3

def update_figure1(aggregated_df):

    # coordinates defining campus shape
    campus_polygon = [
        [38.343309, -122.679879],
        [38.343311, -122.674769],
        [38.346074, -122.672685],
        [38.346182, -122.666775],
        [38.336137, -122.666731],
        [38.336032, -122.679787],
        [38.343309, -122.679879]
    ]

    # campus scattermap trace
    campus_map_trace = go.Scattermap(
        lat=[pt[0] for pt in campus_polygon],
        lon=[pt[1] for pt in campus_polygon],
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 100, 255, 0.1)',
        line=dict(color='blue'),
        hovertext='Sonoma State University',
        hoverinfo='text'
    )

    # load building GeoJSON file
    with open('assets/geo-json-buildings.json', 'r') as file:
        geo_json_buildings = json.load(file)

    # campus choropleth map trace
    choropleth_map_trace = go.Choroplethmap(
        geojson=geo_json_buildings,
        locations=aggregated_df['truncated_location'],
        z=aggregated_df['value'],
        featureidkey="properties.id",
        colorscale="Jet",
        marker_opacity=0.7,
    )

    #figure1 = go.Figure(campus_map_trace)
    figure1 = go.Figure(data=[choropleth_map_trace, campus_map_trace])

    figure1.update_layout(
        map=dict(
            style='satellite-streets',  
            center=dict(lat=38.340931449672006, lon=-122.67307511912622),  
            zoom=15
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return figure1

def update_figure2(aggregated_df):

    figure2 = px.bar(
        aggregated_df,
        x='value',
        y='truncated_location',
        title='Sum of Energy Consumption by Location',
        labels={'value': 'Sum of Value', 'location': 'Location'},
        template='plotly_white',
        hover_name='location'    
    )

    return figure2

def update_figure3(aggregated_df):

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

    return figure3

