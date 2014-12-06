#!/usr/bin/env python

import urllib, re
import bs4
          
def songlyrics(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','-'))
    title = urllib.quote(title.lower().replace(' ','-'))

    try:
        lyrics = urllib.urlopen('http://www.songlyrics.com/%s/%s-lyrics/' % (artist,title))
    except:
        return None
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    lyrics = soup.findAll(attrs= {'id' : 'songLyricsDiv'})
    if not lyrics:
        return None
    else:
        if str(lyrics[0]).startswith("<p class='songLyricsV14 iComment-text' id='songLyricsDiv'></p>"):

            return None
        try:
            return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
        except:
            return None


def lyricsmode(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','_'))
    title = urllib.quote(title.lower().replace(' ','_'))

    try:
        url = 'http://www.lyricsmode.com/lyrics/%s/%s/%s.html' % (artist[0],artist, title)
        lyrics = urllib.urlopen(url)
    except:
        return None 
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    #lyricsmode places the lyrics in a span with an id of "lyrics"
    lyrics = soup.findAll(attrs= {'id' : 'lyrics_text'})
    if not lyrics:
        return None 
    try:
        return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
    except:
        return None  

        
        
def get_lyrics(artist, title):
    lyr = songlyrics(artist, title)
    if not lyr:
        lyr = lyricsmode(artist, title)
    return lyr

        


if __name__ == '__main__':
    test = get_lyrics('Bob Dylan','Blowing in the wind')
    print(test)
    test2 = get_lyrics('test','test')
    print(test2)
