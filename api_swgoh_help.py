"""
Created on Tue Sep  4  2018

@author: martrepodi

Built upon code borrowed from platzman and shittybill
"""

import requests
from json import loads, dumps
import time

class api_swgoh_help():
    def __init__(self, settings):
        self.user = "username=" + settings.username
        self.user += "&password=" + settings.password
        self.user += "&grant_type=password"
        self.user += "&client_id=" + settings.client_id
        self.user += "&client_secret=" + settings.client_secret

        self.token = {}
        self.logged_in = False

        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.endpoints = {'guilds': '/swgoh/guilds',
                          'players': '/swgoh/players',
                          'roster': '/swgoh/roster',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}

        if settings.charStatsApi:
            self.charStatsApi = settings.charStatsApi
        else:
            self.charStatsApi = 'https://crinolo-swgoh.glitch.me/testCalc/api'

        self.verbose = settings.verbose if settings.verbose else False
        self.debug = settings.debug if settings.debug else False
        self.dump = settings.dump if settings.dump else False

        self.data_type = {'guild':'/swgoh/guild/',
                          'player':'/swgoh/player/',
                          'data':'/swgoh/data/',
                          'units':'/swgoh/units',
                          'battles':'/swgoh/battles'}
        
    def _getAccessToken(self):
        if 'expires' in self.token.keys():
            token_expire_time = self.token['expires']
            if token_expire_time > time.time():
                return(self.token)
        signin_url = self.urlBase+self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded"}
        r = requests.request('POST',signin_url, headers=head, data=payload, timeout = 10)
        if r.status_code != 200:
            error = 'Login failed!'
            return  {"status_code" : r.status_code,
                     "message": error}
        response = loads(r.content.decode('utf-8'))
        self.token = { 'Authorization': "Bearer " + response['access_token'],
                       'expires': time.time() + response['expires_in'] - 30}
        return(self.token)

    def fetchAPI(self, url, payload):
        self._getAccessToken()
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        try:
            r = requests.request('POST', data_url, headers=head, data=dumps(payload))
            if r.status_code != 200:
                error = 'Cannot fetch data - error code'
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch data'}
        return data

    def fetchZetas(self):
        try:
            return self.fetchAPI(self.endpoints['zetas'], {})
        except Exception as e:
            return str(e)

    def fetchSquads(self):
        try:
            return self.fetchAPI(self.endpoints['squads'], {})
        except Exception as e:
            return str(e)

    def fetchBattles(self, payload):
        if not payload:
            payload = { "language": "eng_us", "enums": True }
        try:
            return self.fetchAPI(self.endpoints['battles'], payload)
        except Exception as e:
            return str(e)

    def fetchEvents(self, payload):
        if not payload:
            payload = { "language": "eng_us", "enums": True }
        try:
            return self.fetchAPI(self.endpoints['events'], payload)
        except Exception as e:
            return str(e)

    def fetchData(self, payload):
        if type(payload) != dict:
            return({'message': "Payload ERROR: dict expected."})
        if 'collection' not in payload.keys():
            return({'message': "Payload ERROR: No collection element in provided dictionary."})
        try:
            return self.fetchAPI(self.endpoints['data'], payload)
        except Exception as e:
            return str(e)

    def fetchPlayers(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
        except Exception as e:
            return str(e)

    def fetchGuilds(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    def fetchUnits(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['units'], payload)
        except Exception as e:
            return str(e)

    def fetchRoster(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
        except Exception as e:
            return str(e)

class settings():
    def __init__(self, _username, _password, **kwargs):
        self.username = _username
        self.password = _password
        self.client_id = kwargs.get('client_id', '123')
        self.client_secret = kwargs.get('client_secret', 'abc')
        self.charStatsApi = kwargs.get('charStatsApi', '')
        self.verbose = kwargs.get('verbose', False)
        self.debug = kwargs.get('debug', False)
        self.dump = kwargs.get('dump', False)
