import glob
import glob
import json
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
path = data['path_recursive_popularity']
filepath = data['save_path_local_popularity']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)



def main(path):
    folder = path
    files = glob.glob(folder, recursive=True)
    list_songs = []

    for item in files:
        try:
            path = item
            artist, name, popularity, link = retrieve_popularity(path)
            if popularity is not None:
                dict_song = {'artist': artist, 'song': name, 'popularity': popularity, 'link': link}
                list_songs.append(dict_song)
        except:
            print('Error with file: ' + item)

    generate_json(list_songs, filepath)

    #df_popularity = pd.DataFrame(list_songs)
    #df_popularity.to_html(filepath, index=False, classes='table-responsive table-bordered', table_id='table_popularity', border=0, escape=False, justify='center', col_space=100, na_rep='N/A')


def generate_json(list_details, filepath):
    list_details_sorted = sorted(list_details, key=lambda k: k['popularity'])
    final_dict = {"songs": list_details_sorted}

    full_name = os.path.join(filepath, "songs" + ".json")

    with open(full_name, 'w', encoding='utf-8') as file:
        json.dump(final_dict, file)

        file.close()




if __name__ == '__main__':
    main(path)