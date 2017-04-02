import pymysql.cursors
import os
import json
import codecs
from analyze_lyrics import get_sentiment

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='benjamin',
                             db='DropMuse2',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

try:
    # cursor.execute("""DROP TABLE songs;""")
    connection.commit()
except pymysql.err.InternalError:
    pass

sql = """CREATE TABLE IF NOT EXISTS `songs`
(
    ID BIGINT,
    title VARCHAR( 200 ) NOT NULL,
    artist VARCHAR( 200 ) NOT NULL,
    lyrics TEXT,
    album TEXT,
    link TEXT,
    sentiment TEXT,
    PRIMARY KEY ( `ID` )
);"""

cursor.execute(sql)

artists = ['Mitski', 'LinkinPark', 'Beatles', 'TaylorSwift', 'TwentyOnePilots']

for a in artists:
    path = 'Artists/' + a + '/lyrics/'
    for filename in os.listdir(path):
        if(filename == "urls.txt"):
            continue
        f = codecs.open(path + filename, "r", encoding='utf-8')
        title = f.readline().rstrip()
        title = f.readline().rstrip()
        lyrics = f.read()
        if(title == ""):
            f.close()
            continue
        print(title)
        tup = (title.encode('utf-8'),
               a.encode('utf-8'),
               lyrics.encode('utf-8'),
               json.dumps(get_sentiment(a, filename)))
        cursor.execute("INSERT INTO songs(title, artist, lyrics, sentiment) "
                       "VALUES (%s, %s, %s, %s)", tup)
        f.close()

        connection.commit()
