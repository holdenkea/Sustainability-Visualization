from app import app
from layouts.homepage.homepage_layout import layout
import callbacks.graph_callbacks

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)