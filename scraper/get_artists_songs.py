from song_lists import *

cache = "https://web.archive.org/web/"
url = "www.azlyrics.com"

j = 0
for i in mitski:
    lp_urls = []
    print(cache + url + i[1][2:])
