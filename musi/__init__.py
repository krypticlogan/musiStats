import flask
from flask import Flask, request, url_for, session, redirect, render_template
import random as ran
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from ext import *
import flask_login
from flask_login import LoginManager

login_manager = LoginManager()


load_dotenv()

config = dotenv_values()

def generate_key():
    key = ''
    while (len(key) < 31):
        n = ran.randint(0,100)
        key = key + str(n)
    return key

app = Flask(__name__, template_folder='templateFiles',static_folder='static')
''' 
TODO:

1. add user on sign-up: get time created and last logged : DONE
2. find user provider, update user.provider : DONE

 

4. push user to stats screen: DONE
    4.1 get user top songs/tracks/albums DONE

    4.2 collect user data for database and commit


5. format user tracks page, show top songs, artists, albums DONE


6. try to find playlists similar to user

recommendations soon

7. update db tables correctly with time

FEATURES ?

edit username,  Default: provider username

Different pages for logged in and new users (home, user, stats pages) 

'''
app.config.from_mapping(config)


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw=app.config['RDS_PASSWORD'],url='localhost:5500',db='musistatsdb')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

from models import *
db = SQLAlchemy(model_class=Base)

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# Session = scoped_session(sessionmaker(bind=engine))


from queries import Session # db init
from flask_migrate import Migrate # alembic
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# with app.app_context():
#     db.create_all()



from musi import views

app.secret_key = generate_key()
app.config['SESSION COOKIE NAME'] = 'cookie'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0







#login manager
from flask_login import LoginManager

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(user_id)

login_manager.login_view = 'http://127.0.0.1:8000/signin'


# #apis
# SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
# SPOTIPY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
# spotify_scope = "user-read-recently-played"+"%20"+"user-top-read"+"%20"+"user-library-read"+"%20"+"user-read-currently-playing"
# redirect_uri='http://127.0.0.1:8000/stats'
# state = generate_key()

# redirect_uri='https://www.musistats.net/stats'
# #spotify auth


#     ##apple auth
# def apple_auth():
#     return


#     ##soundcloud auth
# def soundcloud_auth():
#     return


