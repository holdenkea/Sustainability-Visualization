from data.csv_source import df

# location and unit lists
location_options = []
unit_options = []

# gets the unique locations and units from the dataframe and sorts them alphabetically
for location in sorted(df['location'].unique()):
    location_options.append({'label': location, 'value': location})

for unit in sorted(df['unit'].unique()):
    unit_options.append({'label': unit, 'value': unit})

# gets unique locations and units from dataframe and turns them into a list for the checklist
default_locations = df['location'].unique().tolist()
default_units = ['kWh']