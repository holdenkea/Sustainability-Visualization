from dash import html, dcc

# empty placeholder graphs
graph1 = dcc.Graph(id='graph1', style={'height': '100%', 'width': '100%'})
graph2 = dcc.Graph(id='graph2')
graph3 = dcc.Graph(id='graph3')

graphs = html.Div([
    # graph 1 and sidebar
    html.Div([
        html.Div([
            html.Label("Map Overlay Type"),
            dcc.RadioItems(
                id='map-overlay-type',
                options=[
                    {'label': 'Choropleth', 'value': 'choropleth' },
                    {'label': 'Bubble', 'value': 'bubble'}
                ],
                value='choropleth',
                labelStyle={'display' : 'block'},
                style={'marginBottom': '10px'}
            )
        ], style={'width': '200px', 'padding': '10px', 'backgroundColor' : "#3c3c81"}),

        dcc.Graph(id='graph1', style={'flex': 1})
    ], style= {
        'gridArea': 'graph1',
        'display': 'flex',
        'flexDirection': 'row',
        'gap': '10px',
    }),

    # graph 2
    html.Div(graph2, style={
        'gridArea': 'graph2',
    }),

    # graph 3
    html.Div(graph3, style={
        'gridArea': 'graph3',
    }),
], style={
    'display': 'grid',
    'gridTemplateColumns': '2fr 1fr',
    'gridTemplateRows': '1fr 1fr',
    'gridTemplateAreas': '''
        "graph1 graph2"
        "graph1 graph3"
    ''',
    'gap': '10px',
    'height': '600px',
    'width': '100%'
})
