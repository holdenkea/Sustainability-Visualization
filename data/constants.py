from data.csv_source import df
import pandas as pd
import json

##################################################################################################
# location options and defaults for filters section
location_options = []

for location in sorted(df['location'].unique()):
    location_options.append({'label': location, 'value': location})

default_locations = df['location'].unique().tolist()

##################################################################################################
# unit options and defaults for filters section
unit_options = []

for unit in sorted(df['unit'].unique()):
    unit_options.append({'label': unit, 'value': unit})

default_units = ['kWh']

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

