import csv
import glob
import os
import re
from difflib import SequenceMatcher

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

from tagger.lastfm import search_lastfm
config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']
path = data['path_recursive_lyrics']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))


songs_path = os.path.join(os.path.dirname(__file__), '../songs.csv')




def retrieve_popularity(filename):
    audio = MP3(filename, ID3=ID3)
    artist = audio.tags.get("TPE1")
    title = audio.tags.get("TIT2")
    filename = filename.split('/')[-1].replace('.mp3', '')
    filename = re.sub(r'^\d+\.', '', filename)
    filename = re.sub('^\d+\s*-\s*', '', filename)

    artist, name, popularity, link = search_spotify(filename, artist, title)
    #artist_lf, name_lf, listener_count_fm = search_lastfm(filename)
    return artist, name, popularity, link
def search_spotify(filename, artist, song):
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
        if ratio > 0.4 and ratio_song > 0.6:
            popularity = track['popularity']
            link = track['external_urls']['spotify']
            if popularity is not None:
                return artist, song, popularity, link

    return artist, song, 0, None
