import dash_table
from dash import html
from ..style import COLUMNS

collection = html.Div([html.H2('Collection', style={'width': '50%', 'display': 'inline-block'}),
                       html.H2(id='all-num',
                               children='',
                               style={'width': '50%', 'display': 'inline-block', 'text-align': 'right'}),
                       dash_table.DataTable(
                           id='collection-table',
                           data=None,
                           columns=[{'id': c, 'name': c} for c in COLUMNS],
                           style_as_list_view=True,
                           style_cell_conditional=[
                               {
                                   'if': {'column_id': c},
                                   'textAlign': 'left'
                               } for c in ['Title', 'Designer(s)']],
                           style_data_conditional=[
                               {
                                   'if': {'row_index': 'odd'},
                                   'backgroundColor': 'rgb(248, 248, 248)'
                               }
                           ],
                           style_header={
                               'backgroundColor': 'rgb(230, 230, 230)',
                               'fontWeight': 'bold'
                           },
                           style_table={'height': 'auto', 'overflowY': 'auto'},
                           sort_action="native",
                           sort_mode='multi',)])
