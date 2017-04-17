from bs4 import BeautifulSoup as bs, SoupStrainer
from bs4 import Comment
import urllib
import requests
import time
import nltk
from gensim import corpora
from lxml.html import fromstring
import lxml.html as PARSER
import os
import re
import sys
import requests
import time
import nltk
from gensim import corpora
import sys
from analyze_lyrics import *
from urllib.request import urlopen
#from find_artist_songs import find_artist_songs
#from analyze_lyrics import get_sentiment
#artist = sys.argv[1]
#response = urllib.request.urlopen(path + 'acrosstheline.html').read()

#
# artists = ['Mitski', 'LinkinPark', 'Beatles', 'TaylorSwift', 'TwentyOnePilots']

# for artist in artists:
#    path = 'Artists/' + artist +'/urls/'
#    for filename in os.listdir(path):
#        print(filename)
#        if(filename=='urls.txt'):
#            continue
#        f = open(path + "../lyrics/" + filename.rstrip('.html') + ".txt", "w")
#

#        soup = bs(open(path + filename), "lxml")
#        title = soup.find_all('b', class_=False)
#        if len(title) == 0:
#            continue
#        f.write(artist + "\n")
#        f.write(re.sub('<.*?>|"', '', str(title[len(title) - 1])))

#        for lyrics in soup.find_all(string=lambda text:isinstance(text,Comment)):
#            if "start of lyrics" in lyrics or "Usage" in lyrics:
#                curr = re.sub('<.*?>|([^\s\w]|_)', '', str(lyrics.parent))
#                f.write(curr)

#                break
#        f.close()
#        print("====================================")
#

def format_artist(artist):
    artist = artist.lower()
    if artist[0:2] == "a ":
        artist = artist.replace("a ", "", 1)
    elif artist[0:4] == "the ":
        artist = artist.replace("the ", "", 1)
    artist = artist.replace(" ", "" , 1)
    artist = re.sub('[^0-9a-zA-Z]+','', artist)
    #[^\x00-\x7F]
    return artist

def format_song(song):
    song = song.lower()
    song = song.replace(" ", "" , 1)
    song = re.sub('[^0-9a-zA-Z]+','', song)
    return song

def get_lyrics_with_urls(urls):
    #TODO
    #urls = ['http://lyrics123.net/snoop-dogg/deeez-nuuuts/']

    ret = []
    for url in urls:
        time.sleep(3)
        print(url)

        response = urlopen(url, timeout = 5)
        content = response.read()
        for lyrics in bs(content,"html.parser", parse_only=SoupStrainer('p')):
            if(lyrics.has_attr('style')):
                lyrics = re.sub('</?br/?>', '\n',str(lyrics))
                lyrics = re.sub('<.*?>', '',str(lyrics))
                lyrics = re.sub('\n',' \n',str(lyrics));
                ret.append(lyrics)
                print(lyrics)
                print(str(get_sentiment(lyrics)))
    return ret

def get_lyrics(artist, song):
    #urls = ['http://lyrics123.net/snoop-dogg/deeez-nuuuts/']

        artist = format_artist(artist)
        #print(artist)
        song = format_song(song)

        time.sleep(1)
        url = "https://web.archive.org/web/20161007001058/http://www.azlyrics.com/lyrics/" +artist + "/" + song  + ".html"
        content = None
        try:
            response = urlopen(url, timeout = 5)
            content = response.read()
        except:
            print(url)
            print("failed\n")
            return None

        soup = bs(content,"html.parser", parse_only=SoupStrainer('div'))
        for l in soup:
            for lyrics in soup.find_all(string=lambda text:isinstance(text,Comment)):
                if "start of lyrics" in lyrics or "Usage" in lyrics:
                    lyrics = re.sub('</?br/?>', '',str(lyrics.parent))
                    lyrics = re.sub('<.*?>', '',str(lyrics))
                    #lyrics = re.sub('\n',' \n',str(lyrics));
                    return str(lyrics)
