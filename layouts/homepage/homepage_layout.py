from dash import html

# layout imports
from layouts.homepage.graphs_layout import graphs
from layouts.homepage.filters import filters

layout = html.Div([
    html.H1("Test Dashboard", style={'textAlign': 'left'}),
    
    # flex container for main dashboards (left), and sidebar (right)
    html.Div([
        
        # graphs section
        html.Div(graphs, style={'flex' : '5', 'padding' : '10px', 'backgroundColor' : "#1c1c30", 'color' : 'white'}),

        # filters section
        html.Div(filters, style={'flex' : '1', 'padding' : '10px', 'backgroundColor' : "#4B4B4F"})
    ], 
    style={'display' : 'flex', 'flexDirection' : 'row', 'width' : '100%'}) 
],
style={
    'backgroundColor': "#171441",  
    'color': 'white',              
})