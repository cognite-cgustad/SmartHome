import requests
import time
import pandas as pd
import os
from os.path import join, exists
from apps.boardgames.config import DATAPATH
import xml.etree.ElementTree as ET


class User(object):
    def __init__(self, username):
        self.username = username
        self.api = BoardGameGeekAPI(username)
        self.user_folder = join(DATAPATH, 'users', username)
        # Data from files
        self.basegames_path = join(self.user_folder, 'basegames.csv')
        self.expansions_path = join(self.user_folder, 'expansions.csv')
        self.file_ids_basegames = []
        self.file_ids_expansions = []
        # Data from query
        self.xml = None
        self.xml_ids_basegames = []
        self.xml_ids_expansions = []

    def query_collection(self):
        """
        Queries bgg for user and check for error tags
        """
        self.xml = self.api.query_bgg_collection()
        self.has_errors()


    def has_errors(self):
        """
        Checks for errors messages
        """
        response = self.xml.get('base_game_items')
        if response.tag != 'errors' or self.xml is None:
            return None
        error_messages = []
        for error in response:
            for message in error:
                error_messages.append(message.text)
        error_message = "\n".join(error_messages)
        return error_message


    def get_xml_ids(self):
        """
        Extracts ids from xml
        """
        if self.xml:
            # Go through basegames
            for item in self.xml['base_game_items']:
                bgg_id = item.attrib['objectid']
                self.xml_ids_basegames.append(bgg_id)
            # Go through expansions
            for item in self.xml['xml_expansions']:
                bgg_id = item.attrib['objectid']
                self.xml_ids_expansions.append(bgg_id)

    def read_file_ids(self):
        """
        Reads all files for the user and adds ids to class instance
        """
        if not exists(self.user_folder):
            os.mkdir(self.user_folder)
        if exists(self.basegames_path):
            df_basegame = pd.read_csv(self.basegame_path)
            self.file_ids_basegames = list(df_basegame["id"])
        if exists(self.expansions_path):
            df_expansions = pd.read_csv(self.expansions_path)
            self.file_ids_expansions = list(df_expansions["id"])

    def compare_basegames(self):
        """
        Compare difference between xml and current file
        """
        return self.file_ids_basegames.sort() == self.xml_ids_basegames.sort()

    def compare_expansions(self):
        """
        Compare difference between xml and current file
        """
        return self.file_ids_expansions.sort() == self.xml_ids_expansions.sort()


class BoardGameGeekAPI(object):
    API_URL = "https://www.boardgamegeek.com/xmlapi2/"


    def __init__(self, bgg_username):
        self.username = bgg_username
        
    def query_bgg(self, type_string, params):
        timeout = 5
        try:
            query_result = requests.get(self.API_URL + type_string, params=params)
        except requests.exceptions.ConnectionError:
            print('Could not get type: ' + type_string)
            print('retrying')
            time.sleep(timeout)
            query_result = requests.get(self.API_URL + type_string, params=params)
            #query_bgg(type_string, params)
        #time.sleep(1)
        
        while query_result.status_code == 202:
            print("Code 202: Board Game Geek has queued your request. Trying again in " + str(timeout) + " seconds.")
            time.sleep(timeout)
            query_result = requests.get(self.API_URL + type_string, params=params)
                    
        while query_result.status_code == 429:
            print("Code 429: Board Game Geek asks you too slow down. Trying again in " + str(timeout) + " seconds.")
            time.sleep(timeout)
            query_result = requests.get(self.API_URL + type_string, params=params)
        print(f"Request result: {query_result}")
        return query_result

    def query_bgg_collection(self):
        print('Querying collection from BoardGameGeek for user ' + self.username)
        params_base = {
            'username': self.username,
            'subtype': 'boardgame',
            'excludesubtype': 'boardgameexpansion',
            'own': 1,
            'stats': 1,
        }
        
        query_result = self.query_bgg('collection', params_base)

        base_game_items = ET.fromstring(query_result.text)
        print(f"XML string: {ET.tostring(base_game_items)}")

        params_expansion = {
            'username': self.username,
            'subtype': 'boardgameexpansion',
            'own': 1,
            'stats': 1,
        }

        query_result = self.query_bgg('collection', params_expansion)

        expansion_items = ET.fromstring(query_result.text)

        xml_collection = {
                'base_game_items' : base_game_items,
                'expansion_items' : expansion_items,
        }

        return xml_collection
    
    def query_bgg_id(self, game_id):
        param = {
                'id': game_id,
                'stats': 1,
                 }   
        query_result = self.query_bgg('thing', param)
        print('\t' + game_id + ': Returned status code ' + str(query_result.status_code))
        return query_result
        
    def query_bgg_ids(self, game_ids):
        print('Querying base games:')
        xml_base_games = dict()
        for game_id in game_ids['base_game_ids']:
            query_result = self.query_bgg_id(game_id)
            base_game_item = ET.fromstring(query_result.text)
            xml_base_games[game_id] = base_game_item
        
        print('Querying expansions:')
        xml_expansions = dict()
        for game_id in game_ids['expansion_ids']:
            query_result = self.query_bgg_id(game_id)
            expansion_item = ET.fromstring(query_result.text)
            xml_expansions[game_id] = expansion_item
        
        xml_games = {
            'xml_base_games' : xml_base_games,
            'xml_expansions' : xml_expansions,
        }
        return xml_games
    
