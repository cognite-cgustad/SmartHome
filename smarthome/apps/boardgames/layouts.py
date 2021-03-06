from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from app import app
from .sidebar import sidebar
from .content.contents import collection
from .content.update_write_data import update_data
from .style import CONTENT_STYLE

boardgames_layout = html.Div([
    # Sidebar
    sidebar,
    # Tabs
    dcc.Tabs(id='boardgame-tab', value='collection', children=[
        # Collection tab
        dcc.Tab(label='Collection', value='collection'),
        # Add/Update user/game data
        dcc.Tab(label='Update/write data', value='userdata')
        ],
    style=CONTENT_STYLE
    ),
    html.Div(id='boardgame-display', style=CONTENT_STYLE),
],
)


# Render tabs
@app.callback(Output('boardgame-display', 'children'),
              Input('boardgame-tab', 'value'))
def render_content(tab):
    if tab == 'collection':
        return collection
    elif tab == 'userdata':
        return update_data
    else:
        return 'Error loading tab'
