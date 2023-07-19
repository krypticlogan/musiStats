import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template
import os
from dotenv import load_dotenv
import random as ran


def load(path=None, file=None):
    load_dotenv(path, file)

load()

#apis
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
spotify_scope = "user-read-recently-played"+"%20"+"user-top-read"+"%20"+"user-library-read"+"%20"+"user-read-currently-playing"
redirect_uri='http://127.0.0.1:5000/stats'

##spotify auth
def spotify_auth():
   # redirect_uri=url_for('spotifyUserLogin',_external=True)
    sp = SpotifyOAuth(client_id =SPOTIFY_CLIENT_ID, client_secret = SPOTIFY_CLIENT_SECRET, redirect_uri=redirect_uri, scope = spotify_scope)
    return sp

def generate_key():
    key = ''
    while (len(key) < 31):
        n = ran.randint(0,100)
        key = key + str(n)
    return key

    ##apple auth
def apple_auth():
    return


    ##soundcloud auth
def soundcloud_auth():
    return

##  
    #app
app = Flask(__name__, template_folder='home/loganj/musiStats/templateFiles/html',static_folder='static')

app.secret_key = generate_key()
app.config['SESSION COOKIE NAME'] = 'cookie'

@app.route('/')#home page
def index():
    return render_template('login.html')

@app.route('/stats', methods=['GET'])
def stats():
    return 'redirect'

@app.route('/user')#for signed-in users
def user():
    return render_template('user.html')

    #redirects and authentications
@app.route('/sp', methods=['POST'])#for spotify sign-ups
def spotifyUserLogin():
    sp = spotify_auth()
    return redirect(os.environ.get('SPOTIFY_AUTH_URL')+'response_type=code&client_id='+sp.client_id+'&scope='+sp.scope+'&redirect_uri='+sp.redirect_uri)

@app.route('/sc')
def scUserLogin():
    sc = soundcloud_auth()
    return 'redirect'

@app.route('/am')
def appleUserLogin():
    am = apple_auth()
    return 'redirect'


#app.run()