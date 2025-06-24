from dash import Input, Output, callback
import plotly.express as px
from data.csv_source import df
from data.constants import geo_json_buildings, building_centers
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# helper functions
# function to truncate names
# def truncate_name(name):
#     if "Green Music Center".lower() in name.lower():
#         return "Green Music Center"
#     elif "Ives Hall".lower() in name.lower():
#         return "Ives Hall"
#     elif "Nichols Hall".lower() in name.lower():
#         return "Nichols Hall"
#     elif "Physical Education".lower() in name.lower():
#         return "Physical Education"
#     elif "Rachel Carson Hall".lower() in name.lower():
#         return "Rachel Carson Hall"
#     elif "Student Health Center".lower() in name.lower():
#         return "Student Health Center"
#     elif "Student Center".lower() in name.lower():
#         return "Student Center"
#     elif "Wine Spectator Learning".lower() in name.lower():
#         return "Wine Spectator Center"
#     else:
#         return None
    
# functions to get building center lon and lat
def get_building_center_lon(name):
    return building_centers.get(name, (None, None))[1]
 
def get_building_center_lat(name):
    return building_centers.get(name, (None, None))[0]

# main callback which updates the three graphs when any of the input ids are changed 
@callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Input('location-filter', 'value'),
    Input('unit-filter', 'value'),
    Input('timestamp-filter', 'start_date'),
    Input('timestamp-filter', 'end_date'),
    Input('map-overlay-type', 'value')
)
def update_graphs(selected_locations, selected_units, start_date, end_date, overlay_type):
    # convert date str to datetime.date 
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date is not None:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # filter dataframe based on filters selected
    filtered_df = df[
        (df['truncated_location'].isin(selected_locations)) & 
        (df['unit'].isin(selected_units)) &
        (df['date_only'] >= start_date) &
        (df['date_only'] <= end_date)
    ]

    if filtered_df.empty:
        print("Filtered DataFrame is empty — returning blank figures.")
        return go.Figure(), go.Figure(), go.Figure()
    
    # group by location and sum up value
    aggregated_df = filtered_df.groupby('truncated_location', as_index=False)['energy_usage'].sum()

    # add column of truncated location name 
    #aggregated_df['truncated_location'] = aggregated_df['location'].apply(truncate_name)

    # add columns for building center lon and lat by building
    aggregated_df['center_lon'] = aggregated_df['truncated_location'].apply(get_building_center_lon)
    aggregated_df['center_lat'] = aggregated_df['truncated_location'].apply(get_building_center_lat)

    # csv for debugging contents of aggregated_df
    aggregated_df.to_csv('temp_agg_df.csv', index=False)

    # update map (plotly graph objects with MapLibre map)
    figure1 = update_figure1(aggregated_df, overlay_type)

    # update plotly bar graph 
    figure2 = update_figure2(aggregated_df)

    # update plotly donut chart 
    figure3 = update_figure3(aggregated_df)

    return figure1, figure2, figure3

def update_figure1(aggregated_df, overlay_type):

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
        fillcolor='rgba(0, 110, 255, 0.08)',
        line=dict(color='navy'),
        hovertext='Sonoma State University',
        hoverinfo='text'
    )

    if overlay_type == 'choropleth':

        # campus choropleth map trace
        choropleth_map_trace = go.Choroplethmap(
            geojson=geo_json_buildings,
            locations=aggregated_df['truncated_location'],
            z=aggregated_df['energy_usage'],
            featureidkey="properties.id",
            colorscale="Aggrnyl",
            marker_opacity=0.7,
            colorbar=dict(
                title="Value",
                tickfont=dict(color='white')  
            )
        )

        figure1 = go.Figure(data=[choropleth_map_trace, campus_map_trace])

    elif overlay_type == 'bubble':

        # normalizing values so unit doesn't affect bubble sizes
        values = aggregated_df['energy_usage']
        min_val = values.min()
        max_val = values.max()

        if max_val > min_val:
            normalized_values = (values - min_val) / (max_val - min_val)
        else:
            normalized_values = np.zeros_like(values) 

        bubble_size = normalized_values * 120 + 30  # scale 0–1 to 30-150 px

        # campus bubble map trace
        bubble_map_trace = go.Scattermap(
            lon=aggregated_df['center_lon'],
            lat=aggregated_df['center_lat'],
            text=aggregated_df['truncated_location'],
            mode='markers',
            marker=dict(
                size=bubble_size,
                color=aggregated_df['energy_usage'],
                colorscale='Aggrnyl',
                opacity=0.7,
                colorbar=dict(title='Value',
                              tickfont=dict(color='white'),
                              )
            )
        )
        figure1 = go.Figure(data=[bubble_map_trace, campus_map_trace])

    figure1.update_layout(
        map=dict(
            style='carto-darkmatter', 
            #style='basic', 
            center=dict(lat=38.340931449672006, lon=-122.67307511912622),  
            zoom=15
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0F2249",  
    )

    return figure1

def update_figure2(aggregated_df):

    figure2 = px.bar(
        aggregated_df,
        x='energy_usage',
        y='truncated_location',
        title='Sum of Energy Consumption by Location',
        labels={'energy_usage': 'Sum of Value', 'location': 'Location'},
        template='plotly_white',
        hover_name='truncated_location',
        color_discrete_sequence=px.colors.sequential.Aggrnyl 
    )

    figure2.update_layout(
        paper_bgcolor="#1A1A1A",
        plot_bgcolor="#272936",
        font=dict(color='white'),
    )

    return figure2

def update_figure3(aggregated_df):

    figure3 = px.pie(
        aggregated_df,
        names='truncated_location',
        values='energy_usage',
        title='Percent of Energy Used by Location',
        hole=0.5,
        hover_name='location'
    )

    # display percentage values and labels
    figure3.update_traces(textinfo='percent+label', rotation=210)

    figure3.update_layout(
        paper_bgcolor="#1A1A1A",
        plot_bgcolor="#272936",
        font=dict(color='white'),
    )

    return figure3

