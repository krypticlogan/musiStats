from auth import *

# spotify functions
def spTopSongsData():
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    sp = spotipy.Spotify(auth_manager=auth)
    access_token = auth.get_cached_token()

    if access_token:
        topSongsData = sp.current_user_top_tracks()['items']
    return topSongsData

def spGetTopSongs(data):
    topSongs = []
    albums = []

    for song in data:
        # keys for songs dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
        print("Song : " + song['name']+"\n")
        name = song['name']
        topSongs.append(name)
        album = spGetTrackInfo(song)
        albums.append(album)
    return topSongs, albums

def spGetTrackInfo(track): # takes track data and returns info
    albumData = track['album']
    (url, height, width) = spGetAlbumPhoto(albumData)

    trackName = track['name']
    albumName = albumData['name']

    info = {
        "track" : trackName,
        "album_name" : albumName,
        "image" : url
        # "lengthInSecs" : length,
        # ""
    }
    return info


def spGetAlbumPhoto(album): # takes album data and gets photo
    albumImage = album['images'][2]

    imageURL = albumImage['url']
    imageHeight = albumImage['height']
    imageWidth = albumImage['width']

    return imageURL, imageHeight, imageWidth
   
