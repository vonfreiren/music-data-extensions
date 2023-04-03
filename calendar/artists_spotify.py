import os
import re
from difflib import SequenceMatcher

import spotipy
import yaml
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from spotipy.oauth2 import SpotifyClientCredentials

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']
path = data['path_recursive_lyrics']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))

def search_audio_features(filename):
    audio = MP3(filename, ID3=ID3)
    artist = audio.tags.get("TPE1")
    song = audio.tags.get("TIT2")
    filename = filename.split('/')[-1].replace('.mp3', '')
    filename = re.sub(r'^\d+\.', '', filename)
    filename = re.sub('^\d+\s*-\s*', '', filename)
    if artist is not None and song is not None:
        artist = str(artist)
        song = str(song)
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
        found_artist = track['artists'][0]['name']
        found_song = track['name']
        ratio = SequenceMatcher(None, artist, found_artist).ratio()
        ratio_song = SequenceMatcher(None, song, found_song).ratio()
        if ratio > 0.6 and ratio_song > 0.6:
            popularity = track['popularity']
            if popularity is not None:
                return artist, song, popularity

    return artist, song, 0


