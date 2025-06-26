from data.csv_source import df
import pandas as pd
import json

# Truncate location helper
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

##################################################################################################
# location options and defaults for filters section
# #location_options = []

# for location in sorted(df['location'].unique()):
#     location_options.append({'label': location, 'value': location})

# default_locations = df['location'].unique().tolist()

df['truncated_location'] = df['location'].apply(truncate_name)

location_grouped = (
    df[df['truncated_location'].notnull()]
    .groupby('truncated_location')['energy_usage']
    .sum()
    .reset_index()
)

location_options = [
    {'label': f"{row['truncated_location']} — {row['energy_usage']:.0f} kWh", 'value': row['truncated_location']}
    for _, row in location_grouped.iterrows()
]
default_locations = [opt['value'] for opt in location_options]

##################################################################################################
# unit options and defaults for filters section
unit_options = []

for unit in sorted(df['unit'].unique()):
    unit_options.append({'label': unit, 'value': unit})

default_units = ['electric(kWh)']

##################################################################################################
# timestamp options, marks (ticks), and options for filters section
timestamp_options = []

# convert to datetime
df['time_stamp'] = pd.to_datetime(df['time_stamp'])

# take out only date
df['date_only'] = df['time_stamp'].dt.date

# get unique dates
timestamp_options = sorted(df['date_only'].unique())

timestamp_marks = {}
for index, timestamp in enumerate(timestamp_options):
    timestamp_marks[index] = timestamp.strftime('%Y-%m-%d')

default_min_timestamp = 0
default_max_timestamp = len(timestamp_options) - 1

##################################################################################################
# load building GeoJSON file
with open('assets/geo-json-buildings.json', 'r') as file:
    geo_json_buildings = json.load(file)

# get lon and lat of building centers from geojson file
building_centers = {}
for feature in geo_json_buildings['features']:
    properties = feature['properties']
    building_id = properties['id']
    lon = properties.get('center_lon')
    lat = properties.get('center_lat')
    building_centers[building_id] = (lat, lon)

