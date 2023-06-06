import glob
import os

import mutagen
import yaml
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from tagger.lyrics import search_lyrics

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')


with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

path = data['path_recursive_lyrics']


def main(path):
    folder = path
    files = glob.glob(folder, recursive=True)
    for item in files:
        path = item
        add_lyrics(path)


def add_lyrics(filename):
    audio = MP3(filename, ID3=ID3)
    artist = audio.tags.get("TPE1")
    title = audio.tags.get("TIT2")
    lyrics = audio.tags.getall('USLT')
    if artist is not None and title is not None:
        if len(lyrics) == 0:

            lyrics_text = search_lyrics(str(title), str(artist))
            if lyrics_text is not None:
                print(filename)
                lyrics = mutagen.id3.USLT(encoding=3, lang=u'eng', desc=u'', text=lyrics_text)
                audio.tags.add(lyrics)
                audio.save()

if __name__ == '__main__':
    main(path)