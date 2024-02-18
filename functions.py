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
        print("Song : " + song['name']+"\n")
        name = song['name']
        topSongs.append(name)
        album = spGetTrackInfo(song)
        albums.append(album)
    # print(albums)
    return topSongs, albums

def spGetTrackInfo(track):
    albumData = track['album']
    # print("Album data keys : " + str(albumData.keys()))
    (url, height, width) = spGetAlbumPhoto(albumData)

    trackName = track['name']
    albumName = albumData['name']

    # print("Album name : " + albumName)


    # albumName = 

    # albumImage = albumData['images'][2]
    # imageURL = albumImage['url']
    # imageHeight = albumImage['height']
    # imageWidth = albumImage['width']

    # print(type(albumImage))
    # print(albumData.keys())
    # print(albumImage)

    album = {
        "track" : trackName,
        "name" : albumName,
        "image" : url
        # "lengthInSecs" : length,
        # ""
    }
    return album


def spGetAlbumPhoto(album):
    albumImage = album['images'][2]
    imageURL = albumImage['url']
    imageHeight = albumImage['height']
    imageWidth = albumImage['width']

    # print(type(albumImage))
    # print(albumData.keys())
    # print("Album Image : " + str(albumImage))
    return imageURL, imageHeight, imageWidth
    # keys for songs dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
   
    
       #data is json returned by spotify
    #    data[]
    # return photo
       
    
    # album = data['album']

    # return album
