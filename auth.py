import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
# from os import load_dotenv, find_dotenv
import random as ran
from musi import app

class Auth():
    pass

class SpotifyAuth(Auth):
    pass

class AppleAuth(Auth):
    pass

class scAuth(Auth):
    pass

# def load(path=None, file=None):
#     load_dotenv(path, file)

# load_dotenv(dotenv_path=find_dotenv(), override=True)


def generate_key():
    key = ''
    while (len(key) < 31):
        n = ran.randint(0,100)
        key = key + str(n)
    return key

# Spotify authourization
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

#with app config
SPOTIPY_CLIENT_SECRET = app.config['SPOTIFY_CLIENT_SECRET']
SPOTIPY_CLIENT_ID = app.config['SPOTIFY_CLIENT_ID']
spotify_scope = "user-read-recently-played"+"%20"+"user-top-read"+"%20"+"user-library-read"+"%20"+"user-read-currently-playing"
redirect_uri='http://127.0.0.1:8000/stats' # change to callback function
state = generate_key()


def spotify_auth():
    #redirect_uri=url_for('spotifyUserLogin',_external=True)
    sp = spotipy.oauth2.SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    return sp