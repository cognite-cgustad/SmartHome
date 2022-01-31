from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps.boardgames.layouts import boardgames_layout
from apps.homepage.layouts import homepage_layout


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/boardgames/':
        return boardgames_layout
    else:
        return homepage_layout


if __name__ == '__main__':
    app.run_server(debug=True)
