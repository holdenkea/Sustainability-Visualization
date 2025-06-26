from dash import html

# layout imports
from layouts.homepage.graphs_layout import graphs
from layouts.homepage.filters import filters

layout = html.Div([
    html.H1("Energy Dashboard", style={
            'fontFamily': '"Orbitron", "Segoe UI", sans-serif',
            'textAlign': 'left',
            'marginLeft': '25px',  
            'marginTop': '10px',
            'marginBottom': '10px',
            'height': '35px'
        }),

    # flex container for main dashboards (left), and sidebar (right)
    html.Div([
        
         # filters section
        html.Div(filters, id='filters-sidebar', style={
            'flex' : '1', 
            'padding' : '10px', 
            'backgroundColor' : "#1B1B1B",
            'height' : '100vh',
            'overflowY' : 'auto'
            
        }),

        # graphs section
        html.Div(graphs, style={
            'flex' : '4',
            'padding' : '10px', 
            'backgroundColor' : "#20212A", 
            'color' : 'white',
        })

    ], 
    style={
        'display' : 'flex', 
        'flexDirection' : 'row', 
        'width' : '100%',
        'height' :'100%'
    }) 
],
style={
    'backgroundColor': "#171441",  
    'color': 'white',    
    'height': '100vh'
})
