from data.csv_source import df
import pandas as pd

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
df['timestamp'] = pd.to_datetime(df['timestamp'])

# take out only date
df['date_only'] = df['timestamp'].dt.date

# get unique dates
timestamp_options = sorted(df['date_only'].unique())

timestamp_marks = {}
for index, timestamp in enumerate(timestamp_options):
    timestamp_marks[index] = timestamp.strftime('%Y-%m-%d')

default_min_timestamp = 0
default_max_timestamp = len(timestamp_options) - 1
