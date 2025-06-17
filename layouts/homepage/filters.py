from dash import html, dcc
from data.constants import location_options, default_locations, unit_options, default_units

# filters section
filters = html.Div([
    html.H4("Filters"),

    html.Div([
        html.Label("Location"),
        dcc.Checklist(
            id='location-filter',
            options=location_options,
            value=default_locations
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Unit"),
        dcc.Checklist(
            id='unit-filter',
            options=unit_options,
            value=default_units
        )
    ])
])
