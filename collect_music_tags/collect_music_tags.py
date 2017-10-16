#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Tested in Python 3

# Sebastian Raschka, 2014
# A command line app for
# downloading popular song tags from last.fm
#
# For help, execute
# ./colect_music_tags.py --help

import pylast
import pandas as pd
import pyprind


class LastFMSong(object):
    def __init__(self, artist, title, last_fm_network):
        self.artist = self.__format_str(artist)
        self.title = self.__format_str(title)
        self.network = last_fm_network
        self.tags = None
        
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
        
    def update(self, artist=None, title=None):
        if artist:
            self.artist = self.__format_str(artist)
        if title:
            self.title = self.__format_str(title)
        
    def get_tags(self):
        try:
            tag_set = set()
            track = self.network.get_track(self.artist, self.title)
            for tag in track.get_top_tags():
                tag_set.add(tag[0].name.lower())
            self.tags = ";".join(tag_set)
        except pylast.WSError: # track not found
            pass 
        return self.tags


def make_table(csv_in, csv_out, last_fm_network):
    df = pd.read_csv(csv_in, sep=',')
    df['Tags'] = pd.Series('', index=df.index)
    
    progress_bar = False
    if df.shape[0] > 1:
        progress_bar = pyprind.ProgBar(df.shape[0])
    
    for row in df.index:
        song = LastFMSong(artist=df.ix[row][df.columns[0]], 
                    title=df.ix[row][df.columns[1]], 
                    last_fm_network=last_fm_network
                    )
        tags = song.get_tags()
        df.ix[row][df.columns[2]] = tags
        if progress_bar:
            progress_bar.update()
    df.to_csv(csv_out)
    

if __name__ == '__main__':
    
    # read user API information from separate file in the same dir.
    from user_auth import API_KEY, API_SECRET, USERNAME, PASSWORD
    import argparse
    
    
    parser = argparse.ArgumentParser(
            description='A command line app for downloading popular song tags from last.fm',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='Example:\n'\
                './collect_music_tags.py -i ./artist_title.csv -o ./out.csv\n\nCSV input format:\n'\
                'Artist,Title\n'\
                'Bob Dylan,blowing in the wind\n'\
                '[...]')


    parser.add_argument('-i', '--input', help='Input CSV file.')
    parser.add_argument('-o', '--output', help='Output CSV file.')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')
    
    args = parser.parse_args()

    last_fm_network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, 
                                   username=USERNAME, password_hash=pylast.md5(PASSWORD))
    

    if not args.input:
        print('Please provide an input CSV file.')
        quit()
    if not args.output:
        print('Please provide an output path for the results.')
        quit()

    
    
    if args.input and args.output:
        make_table(args.input, args.output, last_fm_network)