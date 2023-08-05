#Following imports are for the OpenlabApplicationClient
from __future__ import absolute_import, unicode_literals
from oauthlib.oauth2.rfc6749.parameters import (parse_authorization_code_response,
                          parse_token_response, prepare_grant_uri,
                          prepare_token_request)                          
from oauthlib.oauth2.rfc6749.clients.base import Client
from requests_oauthlib import OAuth2Session, OAuth1Session
from oauthlib.oauth2 import InvalidGrantError
from openlab import credentials

import os
import validators
import json
import time
import inspect
import urllib

#Get the location of the installed OpenLab Library
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#exec credentials to force compile so to recognize any changes to credentials
exec(open(current_directory+"/credentials.py").read())

token_file = "openlab_token.txt"
token_path = os.path.join(current_directory, token_file)

#get the credials/login info needed for logging in/getting token
url = credentials.OPENLAB_URL
refresh_url = url + "/connect/token"
user = credentials.email
key = credentials.api_key
client_id = credentials.client_id

class OpenlabApplicationClient(Client):
    """
    Custom ApplicationClient based on oauthlib's WebApplicationClient in order to pass in custom grant type
    """

    def __init__(self, client_id, code=None, **kwargs):
        super(OpenlabApplicationClient, self).__init__(client_id, **kwargs)
        self.code = code

    def prepare_request_uri(self, uri, redirect_uri=None, scope=None,
                            state=None, **kwargs):
            
        return prepare_grant_uri(uri, self.client_id, 'code', 
                                 redirect_uri=redirect_uri, scope=scope, state=state, **kwargs)

    def prepare_request_body(self, client_id=None, code=None, body='', redirect_uri=None, **kwargs):
        code = code or self.code
        return prepare_token_request('openlab_api_key', code=code, body=body,
                                     client_id=self.client_id, redirect_uri=redirect_uri, **kwargs)

    def parse_request_uri_response(self, uri, state=None):
        response = parse_authorization_code_response(uri, state=state)
        self._populate_attributes(response)
        return response

def token_saver(token):
    """
    Saves the token so it can be used next time
    """
    print("Saving token...")
    with open(token_path, 'w') as f:
        json.dump(token, f)

def get_expire_time():
    """
    Returns the expire time of a token if one exists
    """
    # check to see if a token exists
    has_token = os.path.isfile(token_path)
    if has_token:
         #open the token file and read it
        token = open(token_path,'r')
        token_text = token.read()
        #close the token file
        token.close()

        #convert the json data so that we can search key,value pairings
        j = json.loads(token_text)
        return j['expires_at']
    else:
        print("No token exits")
        return

def token_handler(token, proxies):
    """
    Sets up and returns an Oauth Session that will automatically handle token refreshing
    """
    #validate the url and email
    valid_url=validators.url(url)
    valid_user= validators.email(user)
    if not valid_url:
        raise ValueError('Invalid url: ' + url)
    if not valid_user:
        raise ValueError('Invalid email: ' + user)

    extra = {'client_id' : client_id,
              'key' : key}  
 
    #attempt to create client session to pass back
    client = OpenlabApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client = client, token = token, auto_refresh_url= refresh_url, auto_refresh_kwargs = extra, token_updater = token_saver)
    oauth.proxies = proxies

    return oauth

def check_for_proxies():
    """Checks for environmentally set HTTP_PROXY and HTTPS_PROXY which can be set from a command window.
        Alteranatively you can pass these in as a dictionary to the openlab http_client
        Returns an empty dictionary if none were found"""
    #execute all get proxy requests once or until proxies is not empty 
    proxies = {}
    while proxies == {}:
        proxies = urllib.request.getproxies()
        proxies = urllib.request.getproxies_environment()
        proxies = urllib.request.getproxies_registry()
        break
    return proxies

def get_credentials():
    #get the credials/login info needed for logging in/getting token

    c = dict()
    c['url'] = credentials.OPENLAB_URL
    c['refresh_url'] = url + "/connect/token"
    c['user'] = credentials.email
    c['key'] = credentials.api_key
    c['client_id'] = credentials.client_id
    c['proxies'] = credentials.network_proxies
    c['verify'] = credentials.verify
    return c
    
def create_token(**kwargs):
    credentials = get_credentials()

    #give 1st priority to kwargs passed in
    if 'proxies' in kwargs:
        proxies = kwargs.get('proxies')
            
        #check type
        if type(proxies) is not dict:
            raise TypeError("proxies must be a dictionary")

        #use proxies that were passed in
        proxies = kwargs.get('proxies')
    #give 2nd priority to kwargs in credentials
    elif credentials['proxies']:
        proxies = credentials['proxies']

    else:
        #check for environemntal proxies if none were passed in
        proxies = check_for_proxies()

    client = OpenlabApplicationClient(client_id = credentials['client_id'])
    oauth = OAuth2Session(client = client) #this session will be be overwritten with one containing token details for refreshing, but we need it to fetch an initial token 
    oauth.proxies = credentials['proxies']
    oauth.verify = credentials['verify']

    #create an initial token
    try:
        token = oauth.fetch_token(token_url = url+"/connect/token", key = key, username = user, client_id = client_id)
    except InvalidGrantError:
        print("Invalid Grant Error. Ensure the following inputs in openlab/credentials.py are correct:\n email = {}\n key = {}\n url = {}\n".format(user,key, url))
        return
    #save the token
    token_saver(token)
    return token_handler(token, proxies) #overwrite the oauth so that we can refresh on the first time