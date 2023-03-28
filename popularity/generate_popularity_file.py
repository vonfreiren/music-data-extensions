import os

import pandas as pd
import yaml

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


path_popularity = data['save_path_local_popularity']

def generate_file():

    df_popularity = pd.read_csv('/Users/javier/PycharmProjects/music-automatic-tagger/popularity/songs.csv').sort_values(by=['Popularity'], ascending=False)
    df_popularity.to_html(path_popularity, index=False, classes='table-responsive table-bordered', table_id='table_popularity', border=0)


generate_file()