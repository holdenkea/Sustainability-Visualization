from app import app
from layouts.homepage.homepage_layout import layout
import callbacks.main_graph_callback
import callbacks.map_settings_callback
import callbacks.location_filter_callback

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)