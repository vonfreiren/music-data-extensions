import glob
import glob
import os

import pandas as pd
import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

from popularity.popularity_calculations import retrieve_popularity

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')

with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']
path = data['path_recursive_lyrics']


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


path_popularity = data['save_path_local_popularity']


def main(path):
    folder = path
    files = glob.glob(folder, recursive=True)
    list_songs = []

    for item in files:
        path = item
        artist, name, popularity = retrieve_popularity(path)
        if popularity is not None:
            dict_song = {'Artist': artist, 'Song': name, 'Popularity': popularity}
            list_songs.append(dict_song)

    df_popularity = pd.DataFrame(list_songs)
    df_popularity.to_html(path_popularity, index=False, classes='table-responsive table-bordered', table_id='table_popularity', border=0, escape=False, justify='center', col_space=100, na_rep='N/A')







if __name__ == '__main__':
    main(path)