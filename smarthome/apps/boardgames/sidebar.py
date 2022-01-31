from dash import html
from dash import dcc
from os import listdir
from os.path import isfile, join
from .style import SIDEBAR_STYLE
from .config import DATAPATH
# Load files from user folder

USERS = [f for f in listdir(DATAPATH) if isfile(join(DATAPATH, f))]


user = html.Div([dcc.Dropdown(id='user-select',
                              options=USERS,
                              value=USERS[0])])

search = dcc.Input(id='game-search',
                   value='',
                   type='search',
                   placeholder="Search",
                   size='15')

types = dcc.Dropdown(id='type-select',
                     options=[],
                     value=[],
                     multi=True)

player_count = dcc.Slider(
    id='player-count',
    min=0,
    max=6,
    marks={
        0: 'All',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6+'},
    value=0,
    included=False)

game_length = dcc.RangeSlider(
    id='game-length',
    min=0,
    max=180,
    marks={0: '0',
           30: '30m',
           60: '1h',
           90: '1.5h',
           120: '2h',
           150: '2.5h',
           180: '3h+'},
    value=[0, 180])

average_rating = dcc.RangeSlider(
    id='avg-rating',
    min=5,
    max=10,
    step=None,
    marks={5: '5-',
           6: '6',
           7: '7',
           8: '8',
           9: '9',
           10: '10'},
    value=[5, 10])

weight_rating = dcc.RangeSlider(
    id='weight-rating',
    min=1,
    max=5,
    marks={1: '1',
           2: '2',
           3: '3',
           4: '4',
           5: '5'},
    value=[0, 5.0])


designer = html.Div([html.P(),
                     dcc.Dropdown(id='designer-drop',
                                  options=[],
                                  value=[],
                                  multi=True)])
mechanics = html.Div([html.P(),
                      dcc.Dropdown(id='mechanics-drop',
                                   options=[],
                                   value=[],
                                   multi=True)])

category = html.Div([html.P(),
                     dcc.Dropdown(id='category-drop',
                                  options=[],
                                  value=[],
                                  multi=True)])


checkboxes = dcc.Checklist(id='lang-checkbox',
                           options=[
                               {'label': 'Language independent', 'value': 'LI'},
                           ],
                           value=[])

sidebar = html.Div([
    html.H2('User'),
    user,
    html.H2('Search'),
    search,
    html.H2("Filters", className="display-4"),
    html.Div([html.P(),
              html.H5('Type'),
              types,
              html.H5('Player count'),
              player_count,
              html.H5('Game Length'),
              game_length,
              html.H5('BGG rating'),
              average_rating,
              html.H5('Weight'),
              weight_rating,
              html.H5('Designer'),
              designer,
              html.H5('Mechanics'),
              mechanics,
              html.H5('Category'),
              category,
              checkboxes])],
                        style=SIDEBAR_STYLE)

# Filters
def search_filter(game, keyword):
    if keyword is None:
        return(True)
    elif keyword in game['Title']:
        return(True)
    else:
        return(False)


def type_filter(game, type_):
    if not type_:
        return(True)
    for Type in type_:
        if Type in game['Types']:
            return(True)
    return(False)


def gamelength_filter(game, min_gamelength, max_gamelength):
    if min_gamelength <= game['Playing time'] <= max_gamelength:
        return(True)
    elif max_gamelength == 180 and game['Playing time'] >= 180:
        return(True)
    else:
        return(False)


def rating_filter(game, min_rating, max_rating):
    # Take care of less than 5
    if min_rating == 5 and game['Average rating'] <= 5:
        return(True)
    elif min_rating <= game['Average rating'] <= max_rating:
        return(True)
    else:
        return(False)


def weigth_filter(game, min_weight, max_weigth):
    if min_weight <= game['Weight'] <= max_weigth:
        return(True)
    else:
        return(False)


def designer_filter(game, drop_designers):
    if not drop_designers:
        return(True)
    for designer in game['Designers']:
        if designer in drop_designers:
            return(True)
    return(False)


def mechanics_filter(game, drop_mechanics):
    if not drop_mechanics:
        return(True)
    for designer in game['Mechanics']:
        if designer in drop_mechanics:
            return(True)
    return(False)


def category_filter(game, drop_family):
    if not drop_family:
        return(True)
    for designer in game['Categories']:
        if designer in drop_family:
            return(True)
    return(False)


def opt_rec(game, player_count):
    optimal = reccomended = False
    if player_count == 0:
        return(True, False)
    else:
        if player_count in game['Optimal playercount']:
            optimal = True
        if player_count in game['Reccomended playercount']:
            reccomended = True
    return(optimal, reccomended)


def player_count(game, player_count):
    if game['Min players'] <= player_count <= game['Max players']:
        return(True)
    else:
        return(False)


def LI_fil(game, LI):
    if game['Language dependence'] == 'No necessary in-game text':
        return(True)
    elif LI == []:
        return(True)
    else:
        return(False)


def Filter(full_list, search, type_, players, game_length, rating, weight, designers, mechanics, category, LI):
    # Get list of data
    out_list = list()
    opt_list = list()
    min_gamelength = min(game_length)
    max_gamelength = max(game_length)
    min_rating = min(rating)
    max_rating = max(rating)
    min_weight = min(weight)
    max_weigth = max(weight)
    # Iterate through full list of games
    for game in full_list:
        # Filters
        sat_player = player_count(game, players)
        if players == 0:
            sat_player = True
        sat_search = search_filter(game, search)
        sat_type = type_filter(game, type_)
        sat_gamelength = gamelength_filter(game, min_gamelength, max_gamelength)
        sat_rating = rating_filter(game, min_rating, max_rating)
        sat_weigth = weigth_filter(game, min_weight, max_weigth)
        sat_designer = designer_filter(game, designers)
        sat_mechanics = mechanics_filter(game, mechanics)
        sat_category = category_filter(game, category)
        sat_LI = LI_fil(game, LI)
        optimal, recommended = opt_rec(game, players)
        if sat_player and sat_search and sat_designer and sat_mechanics and sat_category and sat_gamelength and sat_rating and sat_weigth and sat_LI and sat_type:
            out_list.append(game)
            if optimal:
                opt_list.append(game)
    return(out_list, opt_list)
