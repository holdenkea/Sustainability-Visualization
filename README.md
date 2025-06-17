app.py - initializes Dash server

index.py - main file that runs the app and combines all components

layouts/
    - home_layout.py - home UI definitions, calls all of the frontent components in layouts
    - filters.py - the sidebar for filtering graph options

callbacks/
    - graph_callbacks.py - graph functions called by user interaction

data/
    - csv_source.py - reads csv file using pandas
    - normalized_data4.csv - csv data file

Docs
    - link to dcc docs - https://dash.plotly.com/dash-core-components
