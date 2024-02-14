# from flask_app import load
import os
# import psycopg2 as ps
from datetime import datetime
from musi import app
import pytz
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_sqlalchemy import SQLAlchemy


# load()

# python -m flask --app musi db upgrade -- pushes changes to db
# python -m flask --app musi db migrate -- loads changes to db

db = SQLAlchemy(model_class=Base)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw=app.config['RDS_PASSWORD'],url='localhost:5500',db='musistatsdb')
engine = create_engine(DB_URL)
Session = scoped_session(sessionmaker(bind=engine))

session = Session()

users = session.query(User).all()
# print(users)


    


#Connecting to database
# try:
#     conn = ps.connect(
#         # host=RDS_URL,
#         database="musistatsdb",
#         user="postgres",
#         password=RDS_PASSWORD,
#         port=5500)

#     print("Connection Established\n")

# except Exception as e: print(e) 

# cur = conn.cursor()
#Connected

# print("Alter data\n")


# SQL query
inn = """ 
"""

# CREATE TABLE playlist (
#   id integer,
#   title varchar,
#   user_id integer,
#   status varchar,
#   created_at timestamp,
#   PRIMARY KEY (id, user_id)
# );

# CREATE TABLE playlistSong (
#   playlist_id integer,
#   song_id integer,
#   title varchar,
#   PRIMARY KEY (playlist_id, song_id)
# );

# CREATE TABLE playedSong (
#   song_id integer,
#   timePlayed timestamp,
#   user_id integer,
#   PRIMARY KEY (song_id, timePlayed)
# );

# CREATE TABLE savedTrack (
#   id integer,
#   user_id integer,
#   PRIMARY KEY (id, user_id)
# );

# CREATE TABLE track (
#   id integer PRIMARY KEY,
#   artist_id integer,
#   on_album varchar(1),
#   album_id integer,
#   length_in_secs integer,
#   genre1 varchar(20),
#   genre2 varchar(20),
#   genre3 varchar(20)
# );

# CREATE TABLE artist (
#   id integer PRIMARY KEY,
#   genre varchar
# );

# CREATE TABLE album (
#   id integer PRIMARY KEY,
#   name varchar,
#   num_songs integer
# );

# CREATE TABLE provider (
#   id integer PRIMARY KEY,
#   name varchar(12)
# );

# CREATE TABLE genre (
#   id varchar(45) PRIMARY KEY,
#   description varchar(400)
# );

# ALTER TABLE savedTrack ADD FOREIGN KEY (user_id) REFERENCES user (id);

# ALTER TABLE playedSong ADD FOREIGN KEY (user_id) REFERENCES user (id);

# ALTER TABLE artist ADD FOREIGN KEY (id) REFERENCES genre (id);

# ALTER TABLE savedTrack ADD FOREIGN KEY (id) REFERENCES track (id);

# ALTER TABLE track ADD FOREIGN KEY (album_id) REFERENCES album (id);

# CREATE TABLE artist_track (
#   artist_id integer,
#   track_artist_id integer,
#   PRIMARY KEY (artist_id, track_artist_id)
# );

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



# ## adds new user 
# def addUser(name, provider=None):


#     if(provider):
#         query =  """ INSERT INTO users (username, provider, created_at, last_logged) VALUES ('%s', %d, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) """
#         formatted = query % (name, provider)

#     else:
#         query =  """ INSERT INTO users (username, created_at, last_logged) VALUES ('%s', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) """
#         formatted = query % (name)

#     try:
#         cur.execute(formatted);
#         print("adding successful")

#     except Exception as e:
#         print(e)

#     print(formatted)

#     conn.commit();

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

# # execute SQL queries

# def doSQL(query='', function=None):
#     pass
# try :
#     # showTables()
#     # showUsers()
#     # addUser(name = "ant")
#     print("hello")

# except Exception as e: 
#     print(e)

# finally : 
#     cur.close()
#     conn.close()

# print("connection ended")