# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship, registry
from sqlalchemy.ext.declarative import declarative_base

mapper_registry = registry()

Base = mapper_registry.generate_base()

# Base.query = session.query_property()

metadata = Base.metadata


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
    created_at = Column(DateTime, nullable=False) # ser default values
    last_logged = Column(DateTime, nullable=False)
    provider_key = Column(String(50))

    provider1 = relationship('Provider')

    def __init__(name, provider):
        username = name

    def __repr__(self):
        return f'ID: {self.id} Name: {self.username} Provider: {self.provider}'
        


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