#!/usr/bin/env python

# Tested in Python 3
#
# Sebastian Raschka, 2014 (http://sebastianraschka.com)
#
# This work is licensed under a GNU GENERAL PUBLIC LICENSE Version 3
# Please see the GitHub repository (https://github.com/rasbt/datacollect) for more details.
#
# A command line tool to download fantasy soccer statistics from https://www.dreamteamfc.com
#
# For help, execute
# ./collect_fantasysoccer.py --help

import pandas as pd
from bs4 import BeautifulSoup
import bs4
import requests
import os

class MakeSoccerTable(object):
    def __init__(self):
        self.player_dict = {}
        
    def parse_dreamteamfc(self):
        url = 'https://www.dreamteamfc.com/statistics/players/ALL/'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')

        # general player stats
        for td in soup.findAll("td", { "class" : "tabName" }):
            name = td.text.split('Statistics')[-1].strip()
            if name:
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                position, team, vfm, value, points = res
                value = value.strip('m')
                self.player_dict[name] = [name, position, team, vfm, value, points]
        
        # make initial DataFrame
        df = pd.DataFrame.from_dict(self.player_dict, orient='index')
        df.columns = ['name', 'position', 'team', 'vfm', 'value', 'points']
        df[['vfm','value']] = df[['vfm','value']].astype(float)
        df[['points']] = df[['points']].astype(int)
        df.tail()

        # Add player status info
        df['status'] = pd.Series('', index=df.index)
        df['description'] = pd.Series('', index=df.index)
        df['returns'] = pd.Series('', index=df.index)
           
        url = 'https://www.dreamteamfc.com/statistics/injuries-and-cards/ALL/'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')

        for td in soup.findAll("td", { "class" : "tabName2" }):
            name = td.text.split('stats')[-1].strip()
            if name:
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                position, team, status, description, returns = res
                df.loc[df.index==name,['status', 'description', 'returns']] = status, description, returns
        

        # Add player form data
        df['month_points'] = pd.Series(0, index=df.index)
        df['week_points'] = pd.Series(0, index=df.index)        
        
        url = 'https://www.dreamteamfc.com/statistics/form-guide/all'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')

        for td in soup.findAll("td", { "class" : "tabName" }):
            name = td.text.strip()
            if name:
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                try:
                    month_pts, week_pts = float(res[-2]), float(res[-1])
                    df.loc[df.index==name, ['month_points', 'week_points']] = month_pts, week_pts
                except ValueError:
                    pass
        return df
        
        
        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download fantasy soccer statistics from https://www.dreamteamfc.com',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='Example:\n'\
                './collect_fantasysoccer.py -o soccerdata.csv')

    parser.add_argument('-o', '--output', help='Output CSV file.', required=True, type=str)
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')
    
    args = parser.parse_args()
    
    # to test if it can be written to this location before
    # attempting to download
    with open(args.output, 'w'):
        pass
    
    table = MakeSoccerTable()
    df = table.parse_dreamteamfc()
    df.to_csv(args.output, index=False)
