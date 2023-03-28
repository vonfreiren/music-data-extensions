import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TYER, TRCK, APIC
from mutagen.mp3 import MP3
import urllib

from tagger.discogs import retrieve_track_number
from lyrics import search_lyrics


def create_tag(filename, year, artist, album, title, genre, track_no, cover):
    print(filename)
    if genre is None:
        genre = 'Electronic'
    audio = MP3(filename, ID3=ID3)
    audio.delete()
    if audio.tags is None:
        audio.tags = ID3()
    audio.tags.version = (2, 4, 0)

    # add title tag
    audio.tags.add(TIT2(encoding=3, text=title))

    # add artist tag
    audio.tags.add(TPE1(encoding=3, text=artist))

    # add album tag
    audio.tags.add(TALB(encoding=3, text=album))

    # add year tag
    audio.tags.add(TYER(encoding=3, text=str(year)))

    # add genre tag
    audio.tags.add(TCON(encoding=3, text=genre))

    # add track number tag
    if track_no is None:
        track_no = retrieve_track_number(album, artist, title)
    audio.tags.add(TRCK(encoding=3, text=str(track_no)))

    lyrics_text = search_lyrics(title, artist)
    if lyrics_text is not None:

    # Create the USLT tag with the lyrics text and language
        lyrics = mutagen.id3.USLT(encoding=3, lang=u'eng', desc=u'', text=lyrics_text)
        audio.tags.add(lyrics)

    response = urllib.request.urlopen(cover)
    content = response.read()

    audio.save()

    audio = MP3(filename, ID3=ID3)
    # Create an APIC frame with the image data
    apic = APIC(
        encoding=3,  # 3 is for UTF-8
        mime='image/jpeg',
        type=3,  # 3 is for the cover image
        desc='Cover',
        data=content
    )

    # Add the APIC frame to the ID3 tags
    audio.tags.add(apic)

    audio.save()


def update_cover(filename, cover):
    image_uri = cover

    # Download the image data

    response = urllib.request.urlopen(image_uri)
    content = response.read()

    audio = MP3(filename, ID3=ID3)
    # Create an APIC frame with the image data
    apic = APIC(
        encoding=3,  # 3 is for UTF-8
        mime='image/jpeg',
        type=3,  # 3 is for the cover image
        desc='Cover',
        data=content
    )

    # Add the APIC frame to the ID3 tags
    audio.tags.add(apic)

    # Save the changes to the music file
    audio.save()
