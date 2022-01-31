from dash import dcc
from app import app
import dash_bootstrap_components as dbc
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from ..style import CONTENT_STYLE
from ..scrape.get_users_data import User

update_data = html.Div(
    [
        html.Div(id='modal-user', children=[]),
        html.H1('Search for user:'),
        dcc.Input(id='search-user',
                  value='',
                  type='search',
                  placeholder="Enter username",
                  size='15'),
        html.Button('Search Bgg', id='submit-user', n_clicks=0),

    ],
style=CONTENT_STYLE
)


@app.callback(Output('submit-user', 'n_clicks'),
              Output('modal-user', 'children'),
              Input('search-user', 'value'),
              Input('submit-user', 'n_clicks'))
def search_bgg(username, clicked):
    if clicked:
        user = User(username)
        user.query_collection()
        errors = user.has_errors()
        if errors:
            print("Found errors")
            print(errors)
            modal = dbc.Modal(
                [
                    dbc.ModalHeader("Got error(s):"),
                    dbc.ModalBody(errors),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="modal-close", className="ml-auto")
                    ),
                ],
            id="modal",
            is_open=True,
            )
            return 0, modal
    else:
        return 0, []
