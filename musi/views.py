from musi import app, render_template, request, url_for, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import *
from db import *
from models import *
from functions import *

import datetime

global SIGNEDIN
SIGNEDIN = False

CURRENT_TIME = datetime.datetime.now().utcnow()
''' 
TODO:

1. add user on sign-up: get time created and last logged : DONE
2. find user provider, update user.provider : DONE

 

4. push user to stats screen: DONE
    4.1 get user top songs/tracks/albums DONE

    4.2 collect user data for database and commit


5. format user tracks page, show top songs, artists, albums


6. try to find playlists similar to user

recommendations soon

7. update db tables correctly with time

FEATURES ?

edit username,  Default: provider username

Different pages for logged in and new users (home, user, stats pages) 

'''
PROVIDER = ''
PROVIDER_ID = None
@app.route('/')#home page
def index():
    # addUser("logan", CURRENT_TIME)

    print(CURRENT_TIME)
    # users = session.query(User).all()
    # print(users)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print(PROVIDER)
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/stats', methods=['GET'])
def stats():
    auth = Auth()
    if SIGNEDIN:
        if PROVIDER == 'spotify': # spotify users
            auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
            access_token = auth.get_cached_token()
            sp = spotipy.Spotify(auth_manager=auth)
            global code
            code = None

            if access_token: #checks for access token // allows entry
                print("access by access token")
                result = sp.current_user() #gets the current user
                #parsing json data
                USERNAME = (result['display_name'])
                #show page

                # dict_keys(['items', 'total', 'limit', 'offset', 'href', 'next', 'previous'])
        
                topSongData = spTopSongsData()
                topTracks, albums = spGetTopSongs(topSongData)
                ## gets top songs of current user and adds them to list object
                # order : high to low

                # print(numSongs)
                print("Tracks : " + str(topTracks))
                print("Albums : "+ str(albums))

                return render_template('tracks.html', username=USERNAME, topTracks=topTracks, albums=albums)
            else: #no access_token, get code and try again    
                code = request.args.get('code')

                auth.get_access_token(code, as_dict=False)

            print("redirecting")
            return redirect("/stats")
            
        elif PROVIDER == 'sc':
            pass
        elif PROVIDER == 'apple':
            pass

    else:
        return render_template('tracks.html', username="")

@app.route('/user')#for signed-in users
def user():
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    sp = spotipy.Spotify(auth_manager=auth)

    access_token = auth.get_cached_token()
    if access_token: 

        result = sp.current_user()

        USERNAME = (result['display_name'])
        # addUser(USERNAME, )
        userImage = (result['images'][0]['url'])
    
        return render_template('user.html', username=USERNAME, userImage=userImage)
    
    else:
        return render_template('user.html')

    #redirects and authentications
@app.route('/loginsp', methods=['POST'])#for spotify sign-ups
def spotifyUserLogin():
    sp = spotify_auth()
    global PROVIDER
    PROVIDER = 'spotify'
    global SIGNEDIN
    SIGNEDIN = True
    return redirect(app.config['SPOTIFY_AUTH_URL']+'response_type=code&client_id='+sp.client_id+'&scope='+sp.scope+'&redirect_uri='+sp.redirect_uri)
    #return sp.get_auth_response()

@app.route('/sc', methods=['POST'])
def scUserLogin():
    global PROVIDER
    PROVIDER = 'sc'
    #sc = soundcloud_auth()
    return render_template('oops.html')

@app.route('/am',  methods=['POST'])
def appleUserLogin():
    global PROVIDER
    PROVIDER = 'apple'
    #am = apple_auth()
    return render_template('oops.html')



