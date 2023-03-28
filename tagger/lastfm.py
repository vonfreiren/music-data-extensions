import os

import pylast
import requests
import yaml
from bs4 import BeautifulSoup

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

API_KEY = data['last_fm_api_key']
API_SECRET = data['last_fm_api_secret']

def parse_url(url):
    bs4 = BeautifulSoup(url, 'html.parser')


def search_lastfm(filename):

    try:

        tracks = find_filename(filename)

        returned_artist = tracks[0]['artist']
        returned_song = tracks[0]['name']


        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )
        track = network.get_track(returned_artist, returned_song)
        popularity = track.get_listener_count()

        return returned_artist, returned_song, popularity


    except:
        return None, None, None
def find_filename(filename):
    url = 'https://ws.audioscrobbler.com/2.0/?method=track.search&track={0}&api_key={1}&format=json'.format(
        filename, API_KEY)
    information = requests.get(url).json()['results']['trackmatches']['track']
    return information
