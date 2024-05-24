# from flask_app import load
import os
# import psycopg2 as ps
from datetime import datetime
from musi import app
from musi import db
import pytz
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_sqlalchemy import SQLAlchemy
import datetime

'''
1. add users, genres first

1.1 check user email against db, hash and log password

1.2 allow signup if user does not have email

2. add user playlists, artists, general tracks / most things depend on them

3.  add specific tracks, if saved/played track not in tracks then create a new track

'''


# load()

# python -m flask --app musi db upgrade -- pushes changes to db
# python -m flask --app musi db migrate -- loads changes to db

# connecting to db, establishing engine and Session


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw=app.config['RDS_PASSWORD'],url='localhost:5500',db='musistatsdb')
engine = create_engine(DB_URL)
Session = scoped_session(sessionmaker(bind=engine))

session = Session()

# users = session.query(User).all()

# print(users)

## adds a new user @params username, user_email, current_time
def addUser(name, email, password, time):
    mads = User(name, email, password, time, time)
    # with app.app_context():
    try:
        db.session.add(mads)
        print(f'Added User {mads.musi_user}') # format username
        try:
            db.session.commit()
            print("and comitted")
        except Exception as e:
            print("Error committing user to db\n")
            print(e)
    except Exception as e:
        print("Error adding user to db\n")
        print(e)

   
def onUserEntry(user):
    user.last_logged = datetime.datetime.now(tz=datetime.timezone.utc)
    
# def addNewTrack(title, length_in_secs, artist_id, on_album, genre1, album_id=None, genre2=None, genre3=None):

#     onAlbum = str(on_album)

#     if not on_album:
#         query =  """ INSERT INTO track (title, artist_id, on_album, length_in_secs, genre1) VALUES ('%s', %d, %s, %d, '%s') """
#         formatted = query % (title, artist_id, onAlbum, length_in_secs, genre1)
#     else:
#         query =  """ INSERT INTO track (title, artist_id, on_album, album_id, length_in_secs, genre1) VALUES ('%s', %d, %s, %d, %d, '%s') """
#         formatted = query % (title, artist_id, onAlbum, album_id, length_in_secs, genre1)

#     try:
#         cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     print(formatted)
#     conn.commit();

# ##

# def addPlayedTrack(song_id, timePlayed, user_id):
#     query =  """ INSERT INTO playedTrack (song_id, user_id, timePlayed) VALUES (%d, %d, '%s') """
#     formatted = query % (song_id, user_id, timePlayed)

#     try:
#         cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     print(formatted)
#     conn.commit();

# ##

# def addSavedPlaylist(playlist_id,title,user_id,created_on, status=None): 
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     formatted = query % (playlist_id, title, user_id, created_on)

#     try:
#         cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     print(formatted)
#     conn.commit();

# def addPlaylistSong(): 
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     # formatted = query % (playlist_id, title, user_id, created_on)
#                        # NEED TO FIX
#     try:
#         # cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     # print(formatted)
#     conn.commit();

# def addAlbum():
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     # formatted = query % (playlist_id, title, user_id, created_on)
#                        # NEED TO FIX
#     try:
#         # cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     # print(formatted)
#     conn.commit();

# def addArtist():
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     # formatted = query % (playlist_id, title, user_id, created_on)
#                        # NEED TO FIX
#     try:
#         # cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     # print(formatted)
#     conn.commit();

# def addGenre():
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     # formatted = query % (playlist_id, title, user_id, created_on)
#                        # NEED TO FIX
#     try:
#         # cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     # print(formatted)
#     conn.commit();

# def addUserSavedS(): 
#     query =  """ INSERT INTO track (playlist_id, title, user_id, created_on) VALUES (%d, '%s', %d, '%s') """
#     # formatted = query % (playlist_id, title, user_id, created_on)
#                        # NEED TO FIX
#     try:
#         # cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     # print(formatted)
#     conn.commit();

# def getProviderID():
#     global PROVIDER_ID
#     global PROVIDER
    
#     if PROVIDER == 'spotify':
#         PROVIDER_ID = 1
#     elif PROVIDER == 'apple music':
#         PROVIDER_ID = 2
#     elif PROVIDER == 'soundcloud':
#         PROVIDER_ID = 3

# def showTables():
#     print("Tables: \n")
#     cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
#     for table in cur.fetchall():
#         print(table)
#     print("--------------------\n")

# def showUsers():
#     print('users: \n')
#     cur.execute("""SELECT * from users""")
#     for user in cur.fetchall():
#         print(user)
#     print("--------------------\n")