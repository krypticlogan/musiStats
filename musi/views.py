from musi import app, render_template, request, url_for, redirect, flask_login, login_manager, flask
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import *
from queries import *
from models import *
from functions import *
from flask_login import login_user, logout_user, current_user, login_required, login_remembered
import json
import requests
import base64

import datetime
from musi import db

global SIGNEDIN
SIGNEDIN = False

CURRENT_TIME = datetime.datetime.now(tz=datetime.timezone.utc)

PROVIDER = ''
PROVIDER_ID = None
NEW_USER = False

user = None


@app.route('/')#home page
def index():
    print(CURRENT_TIME)
    # users = session.query(User).all()
    # print(users)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print(PROVIDER)
    return render_template('index.html')

@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('confirm-password')
        email = request.form.get('email')

        hashed = hashPw(password)
        hashed_entry = hashed.decode()
        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            with app.app_context():
                try:
                    addUser(username, email, hashed_entry, CURRENT_TIME)
                except Exception as e:
                    print(e)
            
                user = db.session.query(User).filter_by(email=email).first()
                # user = db.session.merge(current_user)
       
        # print(user)
            if user:
                    login_user(user)
                    print("Logged In!")
                    current_user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    print('New : ' + str(current_user.new))
                    flask.flash('New User Created!')
                    return redirect('/login')
        else:
            print('email already associated, login?') # link login
            #show error flash
    return render_template('signup.html')

@app.route('/signin', methods=['POST','GET']) # user signs - up/ logs in 
def signin():
    user = None
    errors = []

    if request.method == 'POST': # once submitted
        if not user:
            user = db.session.query(User).filter_by(email=request.form.get('email')).first()
            if user: # update user.lastLogged
                print("user found, checking password")
                if checkPw(user.password_hash, request.form.get('password')):
                    print('correct pw')
                    login_user(user)
                    flask.flash('Logged in successfully')
                    refresh_token = user.refresh_tok
                    # https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
                    # fix "url has allowed host" for redirect
                    return redirect('/stats')
                
                else: 
                     errors.append("Invalid Password")
                    #  print(errors)
                    #  print('incorrect pw')
                     

            else:
                 errors.append("We don't have an account associated with that email :( Would you like to Sign Up?") # link signup
                 print("incorrect email")
                #  print(errors)
    
    return render_template('signin.html', errors=errors) # initial screen, shows user email and password fields
    

@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    '''check database for user, if user is new, treat new user and add to database, else load user and refresh data
    store user.refresh_tok, access_tok : DONE


    cache user data and dont send multiple requests consecutively
    '''

    user = current_user
    print('New : ' + str(user.new))
    print('Auth : ' + str(user.authenticated))

    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)

    if current_user.is_new():
        print('user is new')
        print("new user added")
        code = request.args.get('code')
        
        access_token = auth.get_access_token(code, as_dict=False, check_cache=False)
        f = open('.cache', "r")
        token_info = json.loads(f.read())
        f.close()
        refresh_token = token_info['refresh_token']
        print(refresh_token)
        print(access_token)
        user.access_tok = access_token
        user.refresh_tok = refresh_token
        user.new = False
        db.session.commit()
 
    '''
    1. find user.provider through callback function from provider login
    2. use provider to decide which route
    3. get saved tracks, playlists, following artists, liked songs
    4. save to db
    '''

    print("trying spotify access")

    if current_user.access_tok: #checks for access token // allows entry
                sp = spotipy.Spotify(auth=current_user.access_tok)
                print("access by access token")
                try:
                    result = sp.current_user()
                    USERNAME = (result['display_name'])


                    userSavedTracksData = spGetUserSavedTracksData(user)
                    savedTracks = spGetSavedTracks(userSavedTracksData)

                    # dict_keys(['items', 'total', 'limit', 'offset', 'href', 'next', 'previous'])
            
                    topSongData = spTopSongsData(current_user)
                    albums = spGetTopSongs(topSongData)

                    # gets top songs of current user and adds them to list object
                    # order : high to low

                    topArtistData = spTopArtistsData(current_user)
                    topArtists, artistImg = spGetTopArtists(topArtistData)
                    return render_template('tracks.html', username=USERNAME, albums=albums, artistImgs=artistImg, topArtists=topArtists)

                except Exception as e:
                    print(e)
                    print('trying to refresh token')

                    ## Refresh access token
                    body = {
                    "grant_type": 'refresh_token',
                    "refresh_token": str(current_user.refresh_tok),
                    }

                    print(body)

                    base = SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET
                    baseBytes = base.encode('ascii')
                    base = base64.b64encode(baseBytes)
                    baseString = base.decode('ascii')

                    header = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization':'Basic ' + baseString
                }
                    
                    response = requests.post(url='https://accounts.spotify.com/api/token',headers=header, data=body)
                    
                    print('post and change')
                    
                    token_info =response.json()
                    print(token_info)
                    print(type(token_info))
                    access_token = token_info['access_token']
                    current_user.access_tok = access_token
                    db.session.commit()
                    return redirect('/stats')  
    #     elif PROVIDER == 'sc':
    #         pass
    #     elif PROVIDER == 'apple':
    #         pass

    else:
        return render_template('tracks.html', username="")

@app.route('/user')#for signed-in users
@login_required

def user():
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)

    # try: auth.validate_token(user.access_tok)

    # except Exception as e:
    #     print(e)
    #     print('validate error')
    #  user.access_tok = auth.refresh_access_token(user.refresh_tok)
        # print(auth.refresh_access_token(user.refresh_tok))
    # sp = spotipy.Spotify(auth_manager=auth)
    sp = spotipy.Spotify(auth=current_user.access_tok)

    try: result = sp.current_user()

    except Exception as e:
        print(e)
        print('trying to refresh')
        body = {
        "grant_type": "refresh_token",
        "refresh_token": str(current_user.refresh_tok),
        "client_id": SPOTIPY_CLIENT_ID
        }

        base = SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET
        base = base64.b64encode(base)

        header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization':'Basic' + base
      }

        params = json.dumps(body)
        # header = json.dumps(header)
        response = requests.post(url='https://accounts.spotify.com/api/token',headers=header, params=params)
        print('post and change')
        token_info = json.loads(response)
        access_token = token_info['access_token']
        current_user.access_tok = access_token
        db.session.commit()
        # sp = spotipy.Spotify(auth=current_user.access_tok)

        result = sp.current_user()
    finally:
        USERNAME = (result['display_name'])
        userImage = (result['images'][0]['url'])

        return render_template('user.html', username=USERNAME, userImage=userImage)
    
  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/index')

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



