from analyze_audio import get_audio_analysis
import string
from get_lyrics import get_lyrics
from analyse_lyrics import get_sentiment
from sqlalchemy import text, create_engine
import os

# TODO:
#   Iterate through database for all songs with lyrics == NULL
#   Try to search for song urls
#   If found, get the lyrics and update the database

artists = []

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', 3306)
DB_DBNAME = os.environ.get('DB_DBNAME', 'DropMuse')
DB_CHARSET = "charset=utf8"
DB_PREFIX = os.environ.get('DB_PREFIX', 'mysql+pymysql://')


def update_songs_table():
    conn_str = "{}{}:{}@{}:{}/{}?{}".format(DB_PREFIX,
                                            DB_USER,
                                            DB_PASS,
                                            DB_HOST,
                                            DB_PORT,
                                            DB_DBNAME,
                                            DB_CHARSET)
    engine = create_engine(conn_str, encoding='utf-8')

    # Query songs that don't have sentiment or lyrics or audio analysis
    sql = text('SELECT id, artist, song, song_url '
               'FROM songs '
               'WHERE lyrics IS NULL OR pos IS NULL OR tempo IS NULL;')

    con = engine.connect()
    result = con.execute(sql).fetchall()

    for res in result:
        song_id = res['id']
        artist = res['artist']
        song = res['song']
        song_url = res['song_url']
        lyrics = get_lyrics(artist, song)
        if(lyrics is None):
            print("Could not find lyrics for " + song)
        sentiment = get_sentiment(lyrics)
        tempo, pitch, harmonic, percussive = get_audio_analysis(song_url)

        printable = set(string.printable)
        lyrics = ''.join([filter(lambda x: x in printable, lyrics)])
        '''
        print(lyrics)
        print(sentiment)
        print(tempo)
        print(pitch)
        print(harmonic)
        print(percussive)
        '''
        sql = text('UPDATE songs '
                   'SET lyrics=:lyrics, pos=:pos, neg=:neg, neu=:neu, '
                   '    compound=:compound, tempo=:tempo '
                   '    pitch=:pitch, harmonic=:harmonic, '
                   '    percussive=:percussive '
                   'WHERE id=:song_id;', autocommit=True)
        con.execute(sql,
                    lyrics=str(lyrics),
                    pos=sentiment['pos'],
                    neg=sentiment['neg'],
                    neu=sentiment['neu'],
                    compound=sentiment['compound'],
                    tempo=tempo,
                    pitch=pitch,
                    harmonic=harmonic,
                    percussive=percussive,
                    song_id=song_id)
