from auth import *

# spotify functions
def spGetTopSongs():
    auth = SpotifyOAuth(client_id =SPOTIPY_CLIENT_ID,client_secret = SPOTIPY_CLIENT_SECRET , redirect_uri=redirect_uri, scope = spotify_scope, state=state)
    sp = spotipy.Spotify(auth_manager=auth)

    access_token = auth.get_cached_token()
    if access_token: 

        topSongs = []
        topSongsData = sp.current_user_top_tracks()['items']
        numSongs = sp.current_user_top_tracks()['total']
                # albums = spGetTopSongs(topSongs)
        for song in topSongsData:
                    print(song['name']+"\n")
                    name = song['name']
                    topSongs.append(name)

    return topSongs
    
    # album = data['album']

    # return album
