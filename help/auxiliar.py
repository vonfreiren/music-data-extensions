def get_search_keyword(song_name):
    if '-' in song_name:
        return '-'
    elif '–' in song_name:
        return '–'
    else:
        return None

def get_search_separation(song_name):
    if '-' in song_name:
        return '-'
    elif '–' in song_name:
        return '–'
    else:
        return None