import os
from difflib import SequenceMatcher

import musicbrainzngs
import yaml
from google_images_search import GoogleImagesSearch

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

api = data['api_google_images']
cx_id = data['cx_id_google_images']
gis = GoogleImagesSearch(api, cx_id)

user_musicbrainz = data['user_musicbrainz']
password_musicbrainz = data['password_musicbrainz']

def search_musicbrainz(filename):

    musicbrainzngs.auth(user_musicbrainz, password_musicbrainz)
    musicbrainzngs.set_useragent("My Application", "1.0", "https://myapplication.com")
    musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)

    # Search for the artist ID
    releases = musicbrainzngs.search_releases(filename)

    max_ratio = 0



    for release in releases['release-list']:
        temp_title = release['title']
        temp_artist = release['artist-credit'][0]['artist']['name']
        if get_artist_song(filename):

            ratio = SequenceMatcher(None, temp_artist + temp_title, filename).ratio()
        else:
            ratio = SequenceMatcher(None, temp_title, filename).ratio()

        if ratio > max_ratio:
            max_ratio = ratio
            title = temp_title
            artist = temp_artist

            first_find = releases['release-list'][0]
            year = first_find['date']
            album = first_find['release-group']['title']
            genre = first_find['release-group']['primary-type']
            album_artist = first_find['artist-credit'][0]['artist']['name']
            # track_no = first_find['medium-list'][0]['track-count'][0]['number']
            track_no = first_find['medium-list'][0]['track-count']
            cover = retrieve_image_cover(artist + " " + title)

    if ratio > 0.2:
        return title, artist, album, year, album_artist, track_no, cover, genre
    else:
        return None, None, None, None, None, None, None, None

def retrieve_image_cover(name):

    search_params = {
        'q': name,
        'num': 1
    }

    # define search params
    gis.search(search_params)

    # results
    gis.results()

    # retrieve the first image
    first_image_url = gis.results()[0].url

    return first_image_url


def get_artist_song(song_name):
    if ' - ' in song_name:
        return True
    return False