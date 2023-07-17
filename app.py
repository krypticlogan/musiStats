import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import os
from dotenv import load_dotenv

load_dotenv()

#apis
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
spotify_scope = "user-read-recently-played"+"%20"+"user-top-read"+"%20"+"user-library-read"+"%20"+"user-read-currently-playing"
redirect_uri='http://127.0.0.1:5000/sp'
##spotify auth
def spotify_auth():
    #redirect_uri=url_for('spotifyUserLogin',_external=True)
    sp = SpotifyOAuth(client_id =SPOTIFY_CLIENT_ID, client_secret = SPOTIFY_CLIENT_SECRET, redirect_uri=redirect_uri, scope = spotify_scope)
    return sp

def generate_key():
    key = "jdsvn3948j"
    return key

##apple auth
def apple_auth():
    return


##soundcloud auth
def soundcloud_auth():
    return

##
sp = spotify_auth()
#app
app = Flask(__name__)

app.secret_key = generate_key()
app.config['SESSION COOKIE NAME'] = 'cookie'

@app.route('/')
def hello():
    return '<h1>musiStats</h1>'

@app.route('/newpage')
def newpage():
    return 'redirect'

@app.route('/user')
def user():
    return 'i need to learn javascript'

@app.route('/sp')
def spotifyUserLogin():
    sp = spotify_auth()
    auth_url = sp.get_authorize_url
    return redirect(os.environ.get('SPOTIFY_AUTH_URL')+'response_type=code&client_id='+SPOTIFY_CLIENT_ID+'&scope='+spotify_scope+'&redirect_uri='+redirect_uri)

app.run()

