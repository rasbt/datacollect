#!/usr/bin/env python

import urllib, re
import bs4
          
def songlyrics(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','-'))
    title = urllib.quote(title.lower().replace(' ','-'))

    try:
        lyrics = urllib.urlopen('http://www.songlyrics.com/%s/%s-lyrics/' % (artist,title))
    except:
        return 'Sorry, could not connect to songlyrics.com.'
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    lyrics = soup.findAll(attrs= {'id' : 'songLyricsDiv'})
    if not lyrics:
        return 'Lyrics not found.'
    else:
        if str(lyrics[0]).startswith("<p class='songLyricsV14 iComment-text' id='songLyricsDiv'></p>"):

            return 'Lyrics not found.'
        try:
            return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
        except:
            return 'Sorry, an error occurred while parsing the lyrics.'





    
if __name__ == '__main__':
    test = songlyrics('Bob Dylan','Blowing in the wind')
    print(test)
