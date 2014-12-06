#!/usr/bin/env python

import urllib, re
import bs4
          
def lyricsmode(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','_'))
    title = urllib.quote(title.lower().replace(' ','_'))

    try:
        url = 'http://www.lyricsmode.com/lyrics/%s/%s/%s.html' % (artist[0],artist, title)
        lyrics = urllib.urlopen(url)
    except:
        return 'Sorry, could not connect to lyricsmode.com.'
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    #lyricsmode places the lyrics in a span with an id of "lyrics"
    lyrics = soup.findAll(attrs= {'id' : 'lyrics_text'})
    if not lyrics:
        return 'Lyrics not found.'
    try:
        return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
    except:
        return 'Sorry, an error occurred while parsing the lyrics.'      
          
          

    
if __name__ == '__main__':
    test = lyricsmode('Bob Dylan','Blowin in the wind')
    print(test)
    test2 = lyricsmode('test','test')
    print(test2)
