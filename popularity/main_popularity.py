import csv
import glob
import os


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




def main(path):
    folder = path
    files = glob.glob(folder, recursive=True)
    with open('../songs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Artist", "Title", "Popularity"])

        for item in files:
            path = item
            artist, name, popularity = retrieve_popularity(path)
            if popularity is not None:
                writer.writerow([artist, name, popularity])
            else:
                print('No popularity found for: ' + str(name) + ' by ' + str(artist))





if __name__ == '__main__':
    main(path)