import pymysql.cursors
import os
from aws_creds import *
import unicodedata
from analyze_lyrics import *
import ast
from bs4 import BeautifulSoup as bs, SoupStrainer
import urllib
import requests
import time
import nltk
from gensim import corpora
import sys
from song_lists import *
from urllib.request import urlopen
from get_lyrics import *
from analyze_audio import get_audio_analysis
import string
import re


#TODO:
#   Iterate through database for all songs with lyrics == NULL
#   Try to search for song urls
#   If found, get the lyrics and update the database

def update_songs_table():

    db_name = "main"
    table = "songs"
    connection = pymysql.connect(host=aws_endpoint,
                                 user=aws_username,
                                 password=aws_password,
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    sql_query = "SELECT idsongs_dev, artist, song, song_url FROM " + table + ";"

    cursor.execute(sql_query)
    result = cursor.fetchall()
    #print(result)

    for res in result:
        tup_id = res['idsongs_dev']
        artist = res['artist']
        song = res['song']
        song_url = res['song_url']
        #print("({}, {} , {}, {})".format(tup_id, artist, song, song_url))
        lyrics = get_lyrics(artist, song)
        if(lyrics is None):
            print("Could not find lyrics for " + song)
        sentiment = get_sentiment(lyrics)
        tempo, pitch, harmonic, percussive = get_audio_analysis(song_url)

        printable = set(string.printable)
        lyrics = list(filter(lambda x: x in printable, lyrics))
        lyrics = ''.join(lyrics)
        lyrics = lyrics.replace('\"', '\'')
        #lyrics = lyrics.encode('utf-8', 'ignore')
        '''
        print(lyrics)
        print(sentiment)
        print(tempo)
        print(pitch)
        print(harmonic)
        print(percussive)
        '''
        #time.sleep(10)
        #sql_update = "UPDATE " + table + " SET lyrics=\'" + lyrics + "\', pos=" + str(sentiment['pos']) + ", neu=" + str(sentiment['neu']) + ", neg=" + str(sentiment['neg']) +  ", compound=" + str(sentiment['compound']) + " WHERE id=" + str(tup_id) + ";"
        sql_update = """UPDATE {} SET lyrics=\"{}\" WHERE idsongs_dev={};""".format(table, str(lyrics), tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET pos={} WHERE idsongs_dev={};".format(table,sentiment['pos'], tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET neg={} WHERE idsongs_dev={};".format(table,sentiment['neg'], tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET neu={} WHERE idsongs_dev={};".format(table,sentiment['neu'], tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET compound={} WHERE idsongs_dev={};".format(table,sentiment['compound'], tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET tempo={} WHERE idsongs_dev={};".format(table,tempo, tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET pitch={} WHERE idsongs_dev={};".format(table, pitch, tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET harmonic={} WHERE idsongs_dev={};".format(table,harmonic, tup_id)
        cursor.execute(sql_update)

        sql_update = "UPDATE {} SET percussive={} WHERE idsongs_dev={};".format(table,percussive, tup_id)
        cursor.execute(sql_update)


        connection.commit()
