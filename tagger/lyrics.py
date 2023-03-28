import os
from difflib import SequenceMatcher

import lyricsgenius
import yaml

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

genius_token = data['token_genius']


def search_lyrics(song, artist):
    genius = lyricsgenius.Genius(genius_token)



    # Search for the lyrics for a song
    song_title = song
    song_artist = artist
    try:
        song = genius.search_song(title=song_title, artist=song_artist, get_full_info=False)
        artist = song.artist
        ratio = SequenceMatcher(None, artist, song_artist).ratio()
        if ratio > 0.8:
            return str(song.lyrics)
    except:
        return None
