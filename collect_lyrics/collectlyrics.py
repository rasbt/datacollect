#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Tested in Python 3

# Sebastian Raschka, 2014
# An interactive command line app for
# downloading lyrics from LyricsWikia.com
#
# For help, execute
# ./collectlyrics.py --help

import urllib
import re
import lxml.html
import unicodedata
import os
import pandas as pd
import pyprind as pp


class Song(object):
    def __init__(self, artist, title):
        self.artist = self.__format_str(artist)
        self.title = self.__format_str(title)
        self.url = None
        self.lyric = None
        
    def __format_str(self, s):
        # remove paranthesis and contents
        s = s.strip()
        try:
            # strip accent
            s = ''.join(c for c in unicodedata.normalize('NFD', s)
                         if unicodedata.category(c) != 'Mn')
        except:
            pass
        s = s.title()
        return s
        
    def __quote(self, s):
         return urllib.parse.quote(s.replace(' ', '_'))

    def __make_url(self):
        artist = self.__quote(self.artist)
        title = self.__quote(self.title)
        artist_title = '%s:%s' %(artist, title)
        url = 'http://lyrics.wikia.com/' + artist_title
        self.url = url
        
    def update(self, artist=None, title=None):
        if artist:
            self.artist = self.__format_str(artist)
        if title:
            self.title = self.__format_str(title)
        
    def lyricwikia(self):
        self.__make_url()
        try:
            doc = lxml.html.parse(self.url)
            lyricbox = doc.getroot().cssselect('.lyricbox')[0]
        except (IOError, IndexError) as e:
            self.lyric = ''
            return self.lyric
        lyrics = []

        for node in lyricbox:
            if node.tag == 'br':
                lyrics.append('\n')
            if node.tail is not None:
                lyrics.append(node.tail)
        self.lyric =  "".join(lyrics).strip()    
        return self.lyric



def make_table(csv_in, csv_out):
    df = pd.read_csv(csv_in, sep=',')
    df['Lyrics'] = pd.Series('', index=df.index)
    
    progress_bar = False
    if df.shape[0] > 1:
        progress_bar = pp.ProgBar(df.shape[0])
    
    for row in df.index:
        song = Song(artist=df.ix[row][df.columns[0]], title=df.ix[row][df.columns[1]])
        lyr = song.lyricwikia()
        df.ix[row][df.columns[2]] = lyr
        if progress_bar:
            progress_bar.update()
    df.to_csv(csv_out)
        
        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download song lyrics from LyricWikia.com',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='Example:\n'\
                './collectlyrics.py -a "Bob Dylan" -t "blowing in the wind"\n\n'\
                './collectlyrics.py -i ./input.csv -o ./output.csv\n\n'\
                'CSV input format:\n\n'\
                'Artist,Title\n'\
                'Bob Dylan,blowing in the wind\n[...]\n\n\n\n')


    parser.add_argument('-a', '--artist', help='Artist name.')
    parser.add_argument('-t', '--title', help='Song title.')
    parser.add_argument('-i', '--input', help='Input CSV file.')
    parser.add_argument('-o', '--output', help='Output CSV file.')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')
    
    args = parser.parse_args()
    
    # quick and dirty argument check
    if args.artist and not args.title:
        print('Please provide a song title.')
    elif args.title and not args.artist:
        print('Please provide an artist name.')   
    if args.input and not args.output:
        print('Please provide an output path for the results.')
    if args.output and not args.input:
        print('Please provide an input CSV file.')
    
    if args.artist and args.title:
        song = Song(artist=args.artist, title=args.title)
        lyr = song.lyricwikia()
        print(lyr)
    
    if args.input and args.output:
        make_table(args.input, args.output)
