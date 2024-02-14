from musi import app, render_template, request, url_for, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import *
from db import *
from models import *
''' 
TODO:

1. add user on sign-up: get time created and last logged
2. find user provider, update user.provider

3. prompt user for password after provider sign-in 
    3.1 (add password to user) 

4. push user to stats screen: 
    4.1 get user top songs/tracks/albums

    4.2 collect user data for database and commit

FEATURES ?

edit username,  Default: provider username

'''
PROVIDER = ''
PROVIDER_ID = None
@app.route('/')#home page
def index():
    session = Session()
    mads = User('maddy')
    with app.app_context():
        try:
            db.session.add(mads)
            print(f'Added User {mads.username}')
            try:
                db.session.commit()
                print("and comitted")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
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
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)


    access_token = auth.get_cached_token()
    sp = spotipy.Spotify(auth_manager=auth)

    if access_token: #checks for access token

        result = sp.current_user() #gets the current user

        #parsing json data
        USERNAME = (result['display_name'])
        
    
        return render_template('tracks.html', username=USERNAME)
    
    else:
     code = request.args.get('code')
     auth.get_access_token(code, as_dict=False)
     

     return redirect("/stats")
    
    

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
    return redirect(app.config['SPOTIFY_AUTH_URL']+'response_type=code&client_id='+sp.client_id+'&scope='+sp.scope+'&redirect_uri='+sp.redirect_uri)
    #return sp.get_auth_response()

@app.route('/sc')
def scUserLogin():
    #sc = soundcloud_auth()
    return render_template('oops.html')

@app.route('/am')
def appleUserLogin():
    #am = apple_auth()
    return render_template('oops.html')



