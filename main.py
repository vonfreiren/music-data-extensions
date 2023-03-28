import glob
import re

import mutagen
import yaml

from tagger.discogs import search_discogs
from tagger.lastfm import search_lastfm
from tagger.musicbrainz import search_musicbrainz
from tagger.spotify import search_spotify
from tagger.tags import create_tag
from youtube import search_youtube

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path_recursive']





def get_metadata(initial_song, initial_artist, initial_album, path):
    song_name = path.split('/')[-1].replace('.mp3', '')
    song_name = re.sub(r'^\d+\.', '', song_name)

    yt_results = search_youtube(song_name)

    artist, song = search_lastfm(song_name)


    name, artist, album, year, album_artist, track_no, cover, genre = search_spotify(song_name, artist, song)
    if name is None:
        name, artist, album, year, album_artist, track_no, cover, genre = search_discogs(song_name, initial_artist, initial_album, path)
        if name is None:
            name, artist, album, year, album_artist, track_no, cover, genre = search_musicbrainz(song_name)
    if name is not None:
        create_tag(path, year, artist, album, name, genre, track_no, cover)




def main(path):
    title = None
    artist = None
    album = None
    folder = path
    files = glob.glob(folder, recursive=True)
    for item in files:
        path = item
        audio = mutagen.File(path)
        if audio.tags is not None:
            title = audio.tags.get("TIT2")
            artist = audio.tags.get("TPE1")
            album = audio.tags.get("TALB")
            genre = audio.tags.get("TCON")
            track_number = audio.tags.get("TRCK")
            if title is not None:
                title = str(title)
            if album is not None:
                album = str(album)
            if artist is not None:
                artist = str(artist)
        get_metadata(title, artist, album, path)







main(path)