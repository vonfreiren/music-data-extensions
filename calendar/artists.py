import re
from datetime import datetime
import os
import urllib

import numpy as np
import pandas as pd
import pylast
import requests
import yaml
from bs4 import BeautifulSoup
from numpy import random

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
with open(config_path) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

API_KEY = data['last_fm_api_key']
API_SECRET = data['last_fm_api_secret']
path_jekyll = data['save_path_local_concerts']
list_details = []

def parse_url(url, artist_name):
    url = url+'/+events'
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    for i in range(1, 4):
        user_agent = str(random.choice((user_agent_list)))
        headers = {'User-Agent': (user_agent)}

    dates = BeautifulSoup(requests.get(url,headers=headers, proxies=urllib.request.getproxies()).content, "html.parser").find_all('td', class_='events-list-item-date')
    list_artists = []
    list_dates = []
    list_locations = []
    list_concerts = []
    list_location_details = []
    for event in dates:
        date = event['content']
        list_dates.append(date)
        artists = event.find_next('td', class_='events-list-item-event').find_all('span')
        for i, artist in enumerate(artists):
            if i == 0:
                concert = artist.text
                list_concerts.append(concert)
            else:
                list_artists.append(artist.text)
        dt = datetime.fromisoformat(date)
# Convert to desired format
        date = dt.strftime("%Y-%m-%d %H:%M:%S %z")
        location_tag = event.findNext('div').findNext('div',  class_='events-list-item-venue--title')
        location = location_tag.text.strip()
        location_details = location_tag.findNext('div').text.strip()
        list_locations.append(location)
        list_location_details.append(location_details)
        event_dict = {'main': artist_name,'date': date, 'artists': list(set(list_artists)), 'location': location, 'location_details': location_details, 'concert': concert}
        list_details.append({'main':artist_name, 'concert': concert, 'date': date, 'artists': ', '.join(list(set(list_artists))), 'location': location, 'location_details': location_details})
        #generate_md(event_dict, path_jekyll)

    df_concerts = pd.DataFrame(list_details)
    if not df_concerts.empty:
        df_concerts['date'] = pd.to_datetime(df_concerts['date']).dt.date
        df_concerts.rename(columns={'main': 'Artist', 'date': 'Date', 'artists': 'Artists', 'location': 'Location', 'location_details': 'Location Details', 'concert': 'Concert'}, inplace=True)
        df_concerts.to_html(path_jekyll, index=False, classes='table-responsive table-bordered', table_id='table_concerts', border=0)





def generate_md(event_dict, filepath):
    main = event_dict['main']
    simplified_date = event_dict['date'].split(' ')[0]
    concert = event_dict['concert']
    emoji_pattern = re.compile(
        "[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F910-\U0001F93F]|[\U0001F980-\U0001F9E0]|[\u200d]|[\u2640-\u2642]",
        flags=re.UNICODE)
    concert = emoji_pattern.sub('<EMOJI>', concert)

    title = main+"_"+simplified_date+"_"+concert

    location = event_dict['location']
    location_details = event_dict['location_details']
    artists = event_dict['artists']
    artists = ', '.join(artists)


    title_quotes = f'"{title}"'
    concert_quotes = f'"{concert}"'
    main_quotes = f'"{main}"'
    location_quotes = f'"{location}"'
    location_details_quotes = f'"{location_details}"'
    artists_quotes = f'"{artists}"'
    full_name = os.path.join(filepath, title_quotes + ".md")
    try:
        with open(full_name, 'w', encoding='utf-8') as file:
            file.write("---")
            file.write('\n')
            file.write("title: "+title_quotes)
            file.write('\n')
            file.write("artist: "+main_quotes)
            file.write('\n')
            file.write("date: "+simplified_date)
            file.write('\n')
            file.write("concert: "+concert_quotes)
            file.write('\n')
            # file.write("background: "+cover)
            # file.write('\n')
            file.write("artists: "+artists_quotes)
            file.write('\n')
            file.write("location: "+location_quotes)
            file.write('\n')
            file.write("location_details: "+location_details_quotes)
            file.write('\n')
            file.write("---")
            file.write('\n')

            file.close()
    except Exception as e:
        print(e)



def get_artists():
    list_artists = pd.read_csv('/Users/javier/PycharmProjects/music-automatic-tagger/popularity/songs.csv')[
        'Artist'].unique().tolist()

    for artist in list_artists:
        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )
        artist = network.get_artist(artist)
        url = artist.get_url()
        if url is not None:
            parse_url(url, artist.get_name())

get_artists()
#url= 'https://www.last.fm/music/Blondie/+events'
#parse_url(url, 'Blondie')