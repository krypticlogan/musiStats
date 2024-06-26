# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship, registry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

mapper_registry = registry()

Base = mapper_registry.generate_base()

# Base.query = session.query_property()

metadata = Base.metadata


# python -m flask --app musi db upgrade -- pushes changes to db
# python -m flask --app musi db migrate -- loads changes to db

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(String(45), primary_key=True)
    description = Column(String(400))


class Provider(Base):
    __tablename__ = 'provider'

    id = Column(Integer, primary_key=True, server_default=text("nextval('provider_id_seq'::regclass)"))
    name = Column(String(12), nullable=False)


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True, server_default=text("nextval('artist_id_seq'::regclass)"))
    name = Column(String(50), nullable=False)
    deezer_id = Column(Integer, nullable=False, unique=True)
    genre = Column(ForeignKey('genre.id'))

    genre1 = relationship('Genre')
    tracks = relationship('Track', secondary='artistOnTrack')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    username = Column(String(25))
    provider = Column(ForeignKey('provider.id'))
    created_at = Column(DateTime, nullable=False, server_default=func.now()) # set default values
    last_logged = Column(DateTime, nullable=False, server_default=func.now())
    provider_key = Column(String(50))
    musi_user = Column(String(20), nullable = False)
    refresh_tok = Column(String)
    access_tok = Column(String)
    email = Column(String, nullable=False, )
    password_hash = Column(String, nullable=False)
    authenticated = Column(Boolean, server_default=text("false"))
    new = Column(Boolean, server_default=text("true"))

    provider1 = relationship('Provider')
    __table_args__ = (UniqueConstraint("email", name="users_email_key"),)

    def __init__(self, name, email, password, created_at, last_logged):
       self.musi_user = name
       self.created_at = created_at
       self.last_logged = last_logged
       self.email = email
       self.password_hash = password

    def __repr__(self):
        return f'ID: {self.id} Name: {self.musi_user} Provider: {self.provider}'
    

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def is_new(self):
        return self.new
        


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True, server_default=text("nextval('album_id_seq'::regclass)"))
    creator = Column(ForeignKey('artist.id'), nullable=False)
    deezer_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    num_songs = Column(Integer, nullable=False)

    artist = relationship('Artist')


class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, server_default=text("nextval('playlist_id_seq'::regclass)"))
    title = Column(String(45), nullable=False)
    user_id = Column(ForeignKey('users.id'), primary_key=True, nullable=False)
    status = Column(String(10))
    created_on = Column(DateTime, nullable=False)

    user = relationship('User')


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True, server_default=text("nextval('track_id_seq'::regclass)"))
    deezer_id = Column(Integer, nullable=False, unique=True)
    title = Column(String(50), nullable=False)
    artist_id = Column(Integer, nullable=False)
    on_album = Column(String(1), nullable=False, server_default=text("0"))
    album_id = Column(ForeignKey('album.id'))
    length_in_secs = Column(Integer, nullable=False)
    genre1 = Column(ForeignKey('genre.id'), nullable=False, unique=True)
    genre2 = Column(ForeignKey('genre.id'))
    genre3 = Column(ForeignKey('genre.id'))

    album = relationship('Album')
    genre = relationship('Genre', uselist=False, primaryjoin='Track.genre1 == Genre.id')
    genre4 = relationship('Genre', primaryjoin='Track.genre2 == Genre.id')
    genre5 = relationship('Genre', primaryjoin='Track.genre3 == Genre.id')
    users = relationship('User', secondary='savedTrack')


t_artistOnTrack = Table(
    'artistOnTrack', metadata,
    Column('artist_id', ForeignKey('artist.id'), primary_key=True, nullable=False),
    Column('track_id', ForeignKey('track.id'), primary_key=True, nullable=False)
)


class PlayedTrack(Base):
    __tablename__ = 'playedTrack'

    song_id = Column(ForeignKey('track.id'), primary_key=True, nullable=False)
    timePlayed = Column(DateTime, primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    song = relationship('Track')
    user = relationship('User')


class PlaylistTrack(Base):
    __tablename__ = 'playlistTrack'

    playlist_id = Column(ForeignKey('playlist.id'), primary_key=True, nullable=False)
    song_id = Column(ForeignKey('track.id'), primary_key=True, nullable=False)
    title = Column(String(50), nullable=False)

    playlist = relationship('Playlist')
    song = relationship('Track')


t_savedTrack = Table(
    'savedTrack', metadata,
    Column('id', ForeignKey('track.id'), primary_key=True, nullable=False),
    Column('user_id', ForeignKey('users.id'), primary_key=True, nullable=False)
)


