from dash import html, dcc
from data.constants import (location_options, default_locations, 
                            unit_options, default_units, 
                            timestamp_options, default_min_timestamp, default_max_timestamp, timestamp_marks)

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
    ]),

    html.Div([
        html.Label("Timeframe"),
        dcc.RangeSlider(
            id='timestamp-filter',
            min=0,
            max=len(timestamp_options) - 1,
            value=[default_min_timestamp, default_max_timestamp],
            marks=timestamp_marks,
            allowCross=False,
            step=None,
            tooltip={"placement": "bottom", "always_visible": False}
        )
    ])
])
