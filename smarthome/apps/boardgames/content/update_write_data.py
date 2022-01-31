from dash import dcc
from app import app
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from ..scrape.get_users_data import User

update_data = html.Div(
    [
        #html.Div(id='alerts-users'),
        html.H1('Search for user:'),
        dcc.Input(id='search-user',
                  value='',
                  type='search',
                  placeholder="Enter username",
                  size='24'),
        html.Button('Search Bgg', id='submit-user', n_clicks=0),

    ],
)


@app.callback(
    [
        Output('alert-users', 'children'),
    ],
    [
        Input('submit-user', 'n_clicks'),
    ],
    [
        State('search-user', 'value'),
    ]
)
def search_bgg(n, username):
    print(n)
    print(username)
    if not n or n % 2 == 0:
        return []
        #Action when OFF
    else:
        return []
        # user = User(username)
        # user.query_collection()
        # errors = user.has_errors()
        # if errors:
            # print("Found errors")
            # print(errors)
            # modal = dbc.Modal(
            #     [
            #         dbc.ModalHeader(dbc.ModalTitle("Got error(s):")),
            #         dbc.ModalBody(errors),
            #         dbc.ModalFooter(
            #             dbc.Button("Close", id="modal-close", className="ml-auto")
            #         ),
            #     ],
            # id="modal",
            # is_open=True,
            # )
            # print(modal)
            
