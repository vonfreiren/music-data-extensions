import glob
import os
import re

import pandas as pd
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
path_jekyll = data['save_path_local_analysis_songs']
list_features_songs = []

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))
def search_audio_features(filename):
    try:
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

        if len(results)>0:
            id = results['tracks']['items'][0]['id']
            features = sp.audio_features(id)
            list_features_songs.append({'artist':artist, 'song':song, 'danceability':features[0]['danceability'], 'energy':features[0]['energy'], 'tempo':features[0]['tempo']})

        df_features = pd.DataFrame(list_features_songs)
        df_features.to_html(path_jekyll, index=False, classes='table-responsive table-bordered', table_id='table_analysis',
                            border=0, escape=False, justify='center', col_space=100, na_rep='N/A')
    except:
        pass

def main(path):
    folder = path
    files = glob.glob(folder, recursive=True)


    for item in files:
        path = item
        search_audio_features(path)



if __name__ == '__main__':
    main(path)