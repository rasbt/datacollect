#!/usr/bin/env python

# Tested in Python 3
#
# Sebastian Raschka, 2014 (http://sebastianraschka.com)
#
# This work is licensed under a GNU GENERAL PUBLIC LICENSE Version 3
# Please see the GitHub repository (https://github.com/rasbt/datacollect) for more details.
#
# A command line tool to download the current Premier League Soccer 
# standings from http://www.espnfc.com/barclays-premier-league/23/table
#
# For help, execute
# ./epl_standings.py --help



import pandas as pd
from bs4 import BeautifulSoup
import bs4
import requests
import os

class GetSoccerStandings(object):
    def __init__(self):
        self.player_dict = {}
        
    def parse_espnfc(self):
        team_dict = {}

        url = 'http://www.espnfc.com/barclays-premier-league/23/table'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        for td in soup.findAll('td', { 'class' : 'pos' }):
            rank = int(td.text)
            res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag) and i.text!='\xa0']
            team_name = res[0].strip()
            values = [int(i) for i in res[1:]]
            team_dict[team_name] = [rank] + values
        
        df = pd.DataFrame.from_dict(team_dict, orient='index')
        df.columns=['Pos','P_ov','W_ov','D_ov','L_ov','F_ov','A_ov',
                    'W_hm','D_hm','L_hm','F_hm','A_hm', 'W_aw',
                    'D_aw','L_aw','F_aw','A_aw','GD','PTS']
        df = df.sort('Pos')
        
        return df
        
    def print_column_legend(self):
        col_legend = '''
        
Column legend:

- Pos: POSITION
- P: GAMES PLAYED 
- W: WINS 
- D: DRAWS 
- L: LOSSES 
- F: GOALS FOR 
- A: GOALS AGAINST 
- GD: GOAL DIFFERENCE 
- PTS: POINTS

suffixes:
- _ov: OVERALL
- _hm: HOME GAMES
- _aw: AWAY GAMES

'''
        print(col_legend)
        
        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download the current Premier League Soccer' \
                        'standings from http://www.espnfc.com/barclays-premier-league/23/table',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='Example:\n'\
                './epl_standings.py -o soccerdata.csv')

    parser.add_argument('-o', '--output', help='Output CSV file.', required=True, type=str)
    parser.add_argument('-l', '--legend', help='Print column legend.', action='store_true', default=False)
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')
    
    args = parser.parse_args()
    
    # to test if it can be written to this location before
    # attempting to download
    with open(args.output, 'w'):
        pass
    

    table = GetSoccerStandings()
    
    if args.legend:
        table.print_column_legend()
    
    
    df = table.parse_espnfc()
    df.to_csv(args.output, index=False)
