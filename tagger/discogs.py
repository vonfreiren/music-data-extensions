import os
import time
from difflib import SequenceMatcher

import discogs_client
import yaml

from help.auxiliar import get_search_keyword
from help.constants import discogs_artists_sort

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')


with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

token = data['token_discogs']


def search_discogs(song_name, initial_artist, initial_album, path):
    try:
        has_title_in_track_name = False
        d = discogs_client.Client('ExampleApplication/0.1', user_token=token)
        keyword = get_search_keyword(song_name)
        if keyword is not None:
            results = d.search(song_name)
            has_title_in_track_name = True

        if initial_album is not None and initial_artist is not None:
            results = d.search(artist=initial_artist, album=initial_album)

        if len(results) > 0:
            time.wait(1)
            name, artist, album, year, artist, track_no, cover, genre = get_values(path, results[0], results, song_name,
                                                                                   has_title_in_track_name)

            return name, artist, album, year, artist, track_no, cover, genre
    except:
        return None, None, None, None, None, None, None, None
    return None, None, None, None, None, None, None, None


def get_values(path, release, results, song_name, has_artist_in_trackname=False):
    found = False
    if hasattr(release, discogs_artists_sort):
        artist = release.artists_sort
    else:
        for value in results:
            if hasattr(value, discogs_artists_sort):
                artist = value.artists_sort
                break
    year = release.year
    style = release.styles[0]
    album = release.title
    genre = release.genres[0]
    cover = release.images[0]['uri']
    max_ratio = 0

    for tracklist in release.tracklist:
        if hasattr(tracklist, 'title'):
            ratio = SequenceMatcher(None, song_name, tracklist.title).ratio()
            if ratio > max_ratio:
                max_ratio = ratio
                name = tracklist.title
                track_no = tracklist.position
                if has_artist_in_trackname:
                    ratio_artist = SequenceMatcher(None, song_name, artist).ratio()
                    if ratio_artist > 0.3:
                        found = True

    if found:
        return name, artist, album, year, artist, track_no, cover, genre
    else:
        return None, None, None, None, None, None, None, None

def retrieve_track_number(artist, album, song_name):
    d = discogs_client.Client('ExampleApplication/0.1', user_token=token)
    results = d.search(artist=artist, album=album, track=song_name)
    return results[0].tracklist[0].position