from auth import *
import bcrypt

# spotify functions

# TRACKS
def spTopSongsData(user): # accesses spotify user and gets top song data
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    # sp = spotipy.Spotify(auth_manager=auth)
    sp = spotipy.Spotify(auth=user.access_tok)
    # access_token = auth.get_cached_token()
    topSongsData = sp.current_user_top_tracks()['items']
    return topSongsData

def spGetTopSongs(json): # takes json data gets top songs for a spotify user
    topSongs = []
    topTrackInfo = []

    for song in json:
        # keys for songs dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
        # print("Song : " + song['name']+"\n")
        name = song['name']
        topSongs.append(name)
        info = spGetTrackInfo(song)
        topTrackInfo.append(info)
    return topTrackInfo

def spGetTrackInfo(track): # takes track data from spotify and returns info
    albumData = track['album']
    (url, height, width) = spGetAlbumPhoto(albumData)

    info = {
        "track" : track['name'],
        "album_name" : albumData['name'],
        "artists" : track['artists'],
        "image" : url
        # "lengthInSecs" : length,
        # ""
    }
    print(info['track'])
    print(info)
    return info


def spGetAlbumPhoto(album): # takes album data and gets photo
    albumImage = album['images'][2]

    imageURL = albumImage['url']
    imageHeight = albumImage['height']
    imageWidth = albumImage['width']

    return imageURL, imageHeight, imageWidth

# ARTISTS

def spTopArtistsData(user):
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    # sp = spotipy.Spotify(auth_manager=auth)
    sp = spotipy.Spotify(auth=user.access_tok)
    # access_token = auth.get_cached_token()
    # if access_token:
    topArtistData = sp.current_user_top_artists()['items']
    return topArtistData


def spGetTopArtists(json):
    topArtistsInfo = []
    artistImg = []
    for artist in json:
        # keys for songs dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
        # print("Artist : " + artist['name']+"\n")
        name = artist['name']
        info = spGetArtistInfo(artist)
        topArtistsInfo.append(info)

        # img = spGetArtistInfo(artist)
        # artist.append(img)

    return topArtistsInfo, artistImg

def spGetArtistInfo(artist):
    # albumData = artist['album']
    # (url, height, width) = spGetAlbumPhoto(albumData)

    artistName = artist['name']
    (url, height, width) = spGetArtistPhoto(artist)

    info = {
        "name" : artistName,
        "image": url
        # "album_name" : albumName,
        # "image" : url
        # "lengthInSecs" : length,
        # ""
    }
    return info

def spGetArtistPhoto(artist):
    artistImage = artist['images'][2]

    imageURL = artistImage['url']
    imageHeight = artistImage['height']
    imageWidth = artistImage['width']

    return imageURL, imageHeight, imageWidth


# def spLikedSongsData(user):
#     sp = spotipy.Spotify(auth=user.access_tok)
#     data = None
#     return data

def spGetUserArtists(user):
    sp = spotipy.Spotify(auth=user.access_tok)
    data = None
    return data

def spGetUserSavedTracksData(user):
    sp = spotipy.Spotify(auth=user.access_tok)

    savedTrackData = sp.current_user_saved_tracks(limit=50)['items']
    # print(savedTrackData)
    return savedTrackData

def spGetSavedTracks(data):
    savedTrackInfo = []
    print(data[0]['track'].keys())
    for track in data:
        # print(track)
        info = spGetTrackInfo(track['track'])
        savedTrackInfo.append(info)

    return savedTrackInfo

    

def spGetUserPlaylists(user):
    sp = spotipy.Spotify(auth=user.access_tok)
    data = None
    return data


def spGetUserPlayedTracks(user):
    sp = spotipy.Spotify(auth=user.access_tok)
    data = None
    return data



def hashPw(password):
    password = str(password)
    encodePw = password.encode()
    return bcrypt.hashpw(encodePw, bcrypt.gensalt(rounds=8))

def checkPw(hashed ,entered_password):
    entered_password = str(entered_password)
    # hashBytes = user_hash.encode('utf-8')
    # hashed = hashed.decode()
    hashed = str(hashed)
    return bcrypt.checkpw(entered_password.encode(), bytes(hashed.encode('utf-8')))



