from flask import Flask, request, url_for, session, redirect, render_template
import random as ran
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from ext import *
load_dotenv()

config = dotenv_values()

def generate_key():
    key = ''
    while (len(key) < 31):
        n = ran.randint(0,100)
        key = key + str(n)
    return key

app = Flask(__name__, template_folder='templateFiles',static_folder='static')
app.config.from_mapping(config)

from musi import views

app.secret_key = generate_key()
app.config['SESSION COOKIE NAME'] = 'cookie'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0






DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw=app.config['RDS_PASSWORD'],url='localhost:5500',db='musistatsdb')



app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL




app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

from models import *



# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# Session = scoped_session(sessionmaker(bind=engine))


from db import db, Session
from flask_migrate import Migrate


migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# with app.app_context():
#     db.create_all()



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


