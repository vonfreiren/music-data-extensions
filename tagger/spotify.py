import os

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')


with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))


def search_spotify(filename, artist, song):
    if artist is not None and song is not None:
        results = sp.search(q='artist:' + artist + ' track:' + song, type='track')
        if len(results['tracks']['items']) == 0:
            results = sp.search(q=filename, limit=1)
            if len(results['tracks']['items']) == 0:
                results = sp.search(q=song, limit=1)

    else:
        results = sp.search(q=filename, limit=1)
        if len(results['tracks']['items']) == 0:
            results = sp.search(q=song, limit=1)

    for idx, track in enumerate(results['tracks']['items']):
        name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        year = track['album']['release_date'][0:4]
        album_artist = track['album']['artists'][0]['name']
        if len(track['album']['artists'])>1:
            album_artist_2 = track['album']['artists'][1]['name']
        track_no = track['track_number']
        cover = track['album']['images'][0]['url']

        return name, artist, album, year, album_artist, track_no, cover, None

    return None, None, None, None, None, None, None, None

