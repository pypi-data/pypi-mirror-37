#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import json
import argparse 
parser = argparse.ArgumentParser(prog = "./anime",description='Unoffical Api for Finding Your Favorite Anime')
parser.add_argument('anime_name', metavar='anime_name', type=str, nargs=1,
                    help='The name of the anime or the first part of it ')
parser.add_argument('--page','-p', metavar='P', type=str, nargs=1,
                    help='The Page number of the search query',default="1")
args = parser.parse_args()

### this base Url For the Api
base_url = 'https://www1.gogoanime.sh/anime-list-'
query = args.anime_name[0]
page = args.page[0]
with requests.get(base_url+query+'?page='+page) as page_response:
    soup = BeautifulSoup(page_response.content, 'html.parser')
    count = soup.findAll("ul",{"class": "pagination-list"})
    try:
        page_count = len(count[0].findAll('li'))
    except:
        page_count=1
    anime =soup.findAll("ul",{"class": "listing"})
    anime_count = anime[0].findAll('a')
    num = len(anime[0].findAll('a'))
    json_o = {'Query':query,'anime_count':len(anime_count),'current_page':page,'number_of_pages':page_count,'animelist':{}}
    for i in xrange(num):
        json_o['animelist'][i]={'title':anime_count[i].string,'link':'https://www1.gogoanime.sh'+anime_count[i].get('href')}
    print json.dumps(json_o,indent=4)
