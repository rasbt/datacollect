#!/usr/bin/env python

# A command line tool to download the current Premier League Soccer data
# Tested in Python 3
#
# Sebastian Raschka, 2014 (http://sebastianraschka.com)
#
# Last updated: 12/23/2014
#
# This work is licensed under a GNU GENERAL PUBLIC LICENSE Version 3
# Please see the GitHub repository (https://github.com/rasbt/datacollect) for more details.
#
#
#
# For help, execute
# ./collect_epl.py --help



import pandas as pd
from bs4 import BeautifulSoup
import bs4
import requests
import os

class SoccerData(object):
    def __init__(self):
        self.df_general_stats = None
        self.df_team_standings = None
        self.df_injury_data = None
        self.home_away = None
        self.player_form = None
        self.team_form = None
        self.team_lineups = None
        self.top_scorer = None
        self.top_assists = None
    
    def get_all(self):
        self.get_general_stats()
        self.get_team_standings()
        self.get_injury_data()
        self.get_home_away_data()
        self.get_player_form_data()
        self.get_team_form_data()
        self.get_team_lineups()
        self.get_top_scorer()
        self.get_top_assists()
        
    def to_csv(self, target_dir, print_out=True):
        data = [self.df_general_stats, self.df_team_standings, 
                self.df_injury_data, self.home_away, self.player_form, 
                self.team_form, self.team_lineups, self.top_scorer, self.top_assists]
        
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
            
        names = ['dreamteamfc', 'espn_teamstats', '365stats', 'transfermarkt', 
                 'telegraph', 'mpremierleague', 'fantasyfootballscout', 'espn_scorer', 'espn_assists']    
            
        for df, name in zip(data, names):
            name = os.path.join(target_dir, '%s.csv' % name)
            if type(df) == pd.core.frame.DataFrame:
                df.to_csv(name, index=False)
                if print_out:
                    print('written %s'  % name)
            else:
                if print_out:
                    print('\nNOT written %s\n' % name)
                
        return True
            
    
    def get_general_stats(self, print_out=True):
        
        # Download general statistics
        player_dict = {}

        url = 'https://www.dreamteamfc.com/statistics/players/ALL/'

        if print_out:
            print('Getting general statistics from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        name_list = []

        for td in soup.findAll('td', { 'class' : "tabName" }):
            name = td.text.split('Statistics')[-1].strip()
            if name:
                name_list.append(name)
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                position, team, vfm, value, points = res
                value = value.strip('m')
                player_dict[name] = [name, position, team, vfm, value, points]
                
        df = pd.DataFrame.from_dict(player_dict, orient='index')
        df.columns = ['name', 'position', 'team', 'vfm', 'value', 'pts']
        df[['vfm','value']] = df[['vfm','value']].astype(float)
        df[['pts']] = df[['pts']].astype(int)
        
        # Add injury and card information
        
        df['status'] = pd.Series('', index=df.index)
        df['description'] = pd.Series('', index=df.index)
        df['returns'] = pd.Series('', index=df.index)
        
        url = 'https://www.dreamteamfc.com/statistics/injuries-and-cards/ALL/'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')

        name_list = []

        for td in soup.findAll('td', { 'class' : 'tabName2' }):
            name = td.text.split('stats')[-1].strip()
            if name:
                name_list.append(name)
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                position, team, status, description, returns = res
                df.loc[df.index==name,['status', 'description', 'returns']] = status, description, returns
        
        
        # Add player form information
        
        df['month_pts'] = pd.Series(0, index=df.index)
        df['week_pts'] = pd.Series(0, index=df.index)
        
        url = 'https://www.dreamteamfc.com/statistics/form-guide/all'
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
            
        soup = BeautifulSoup(r.text, 'html5lib')

        name_list = []

        for td in soup.findAll('td', { 'class' : 'tabName' }):
            name = td.text.strip()
            if name:
                name_list.append(name)
        
                res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
                try:
                    month_pts, week_pts = float(res[-2]), float(res[-1])
                    df.loc[df.index==name, ['month_pts', 'week_pts']] = month_pts, week_pts
                except ValueError:
                    pass
                    
        # Reordering the columns

        df = df[['name', 'position', 'team', 'vfm', 'value', 'pts', 'month_pts', 
                 'week_pts', 'status', 'description', 'returns']]
        
        self.df_general_stats = df
        
        return df
        
        
            
    def get_team_standings(self, print_out=True):
        
        url = 'http://www.espnfc.com/barclays-premier-league/23/table'
        
        if print_out:
            print('Getting team standings from %s ...' % url)
        
        team_dict = {}
                
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        for td in soup.findAll('td', { 'class' : 'pos' }):
            rank = int(td.text)
            res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag) and i.text!='\xa0']
            team = res[0].strip()
            values = [int(i) for i in res[1:]]
            team_dict[team] = [rank] + values
        
        df = pd.DataFrame.from_dict(team_dict, orient='index')
        cols = ['Pos','P_ov','W_ov','D_ov','L_ov','F_ov','A_ov',
                    'W_hm','D_hm','L_hm','F_hm','A_hm', 'W_aw',
                    'D_aw','L_aw','F_aw','A_aw','GD','PTS']
        df.columns = cols
        df = df.sort('Pos')
        df['team'] = df.index
        df = df[['team']+cols] # reorder columns
        
        self.df_team_standings = df
        
        return df
        
        
        
    def get_injury_data(self, print_out=True):

        url = 'http://365stats.com/football/injuries'
        
        if print_out:
            print('Getting injury data from %s ...' % url)
        
        
        injury_dict = {}
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        

        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        for td in soup.findAll('td', { 'nowrap' : 'nowrap' }):
            name = td.text.split()
            player_info = ['%s, %s' % (' '.join(name[1:]), name[0])]
            for i in td.next_siblings:
                if isinstance(i, bs4.Tag):
                    player_info.append(i.text)
            injury_dict[player_info[0]] = player_info[1:3]
            
        df = pd.DataFrame.from_dict(injury_dict, orient='index')
        df.columns=['injury', 'returns']
        df['name'] = df.index
        df = df[['name', 'injury', 'returns']]
        
        self.df_injury_data = df
        
        return df



    def get_home_away_data(self, print_out=True):

        url = 'http://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1'
        
        if print_out:
            print('Getting home/away data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        # Find tab for the upcoming fixtures
        tab = 'spieltagtabs-2'
        div = soup.find('div', { 'id' : tab })
        tit = div.findAll('a', { 'class' : 'ergebnis-link' })
        if len(tit) > 0:
            tab = 'spieltagtabs-3'

        # Get fixtures
        home = []
        away = []

        div = soup.find('div', { 'id' : tab })
        for t in div.findAll('td', { 'class' : 'text-right no-border-rechts no-border-links' }):
            team = t.text.strip()
            if team:
                home.append(team)
        for t in div.findAll('td', { 'class' : 'no-border-links no-border-rechts' }):
            team = t.text.strip()
            if team:
                away.append(team)

        df = pd.DataFrame(home, columns=['home'])
        df['away'] = away
        self.home_away = df
        return df



    def get_top_scorer(self, print_out=True):

        url = 'http://www.espnfc.com/barclays-premier-league/23/statistics/scorers'
        
        if print_out:
            print('Getting top scorer data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        
        player_dict = {}

        for td in soup.findAll('td', { 'headers' : 'player' }):
            name = td.text
            team, goals = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag) and i.text!='\xa0']
            player_dict[name] = [team, int(goals)]
    
        df = pd.DataFrame.from_dict(player_dict, orient='index')
        df['name'] = df.index
        df.columns = ['team', 'goals', 'name']
        df = df[['name', 'team', 'goals']]
        df.sort('goals', ascending=False, inplace=True)
        
        self.top_scorer = df
        return df


    def get_top_assists(self, print_out=True):

        url = 'http://www.espnfc.com/barclays-premier-league/23/statistics/assists'
        
        if print_out:
            print('Getting top assists data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        
        player_dict = {}

        for td in soup.findAll('td', { 'headers' : 'player' }):
            name = td.text
            team, assists = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag) and i.text!='\xa0']
            player_dict[name] = [team, int(assists)]
    
        df = pd.DataFrame.from_dict(player_dict, orient='index')
        df['name'] = df.index
        df.columns = ['team', 'assists', 'name']
        df = df[['name', 'team', 'assists']]
        df.sort('assists', ascending=False, inplace=True)
        
        self.top_assists = df
        return df




    def get_player_form_data(self, print_out=True):
                
        url = 'https://fantasyfootball.telegraph.co.uk/premierleague/players/'
        
        if print_out:
            print('Getting player form data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        player_dict = {}

        for t in soup.findAll('td', { 'class' : 'first' }):
            player = t.text.strip()
            player_dict[player] = []
            for s in t.next_siblings:
                if isinstance(s, bs4.Tag):
                    player_dict[player].append(s.text)

        # parse the player dictionary
        df = pd.DataFrame.from_dict(player_dict, orient='index')

        # make name column
        df['name'] = df.index

        # assign column names and reorder columns
        df.columns = ['team', 'salary', 'pts/salary', 'week_pts', 'total_pts', 'name']
        df = df[['name', 'team', 'salary', 'pts/salary', 'week_pts', 'total_pts']]

        # parse data into the right format
        df['salary'] = df['salary'].apply(lambda x: x.strip('£').strip(' m'))
        df[['salary', 'pts/salary']] = df[['salary', 'pts/salary']].astype(float)
        df[['week_pts', 'total_pts']] = df[['week_pts', 'total_pts']].astype(int)
    
    
        url = 'https://fantasyfootball.telegraph.co.uk/premierleague/formguide/'
        r  = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        df['6week_pts'] = pd.Series(0, index=df.index)

        for t in soup.findAll('td', { 'class' : 'first' }):
            player = t.text.strip()
            if player:
                week6 = t.parent.find('td', { 'class' : 'sixth last' })
                df.loc[df['name'] == player, '6week_pts'] = week6.text

        self.player_form = df
        return df
        
        
        
    def get_team_form_data(self, print_out=True):

        
        url = 'http://m.premierleague.com/en-gb/form-guide.html'
        
        if print_out:
            print('Getting team form data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        team_dict = {}

        for d in soup.findAll('td', { 'class' : 'col-pos' }):
            if len(team_dict) > 20:
                break
            pos = d.text
            for e in d.next_siblings:
                if isinstance(e, bs4.Tag):
                    if 'class' in e.attrs and 'col-club' in e.attrs['class']:
                        club = e.text
                        team_dict[club] = pos
                        break

        df = pd.DataFrame.from_dict(team_dict, orient='index')
        
        df.columns = ['position-last-6-games']
        df['team'] = df.index
    
        self.team_form = df
        return df    
        
        
    def get_team_lineups(self, print_out=True):
        
        url = 'http://www.fantasyfootballscout.co.uk/team-news/'
        
        if print_out:
            print('Getting team form data from %s ...' % url)
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        
        except requests.exceptions.ReadTimeout:
            print('\nServer not available. Skipped %s\n' % url)
            return
        
        soup = BeautifulSoup(r.text, 'html5lib') 
        # Note: html5lib deals better with broken html than lxml

        team_dict = {}

        for li in soup.findAll('li'):
            for h2 in li.findAll('h2'):
                team = h2.text
                team_dict[team] = []
                for p in li.findAll('span', { 'class' : 'player-name' }):
                    player = p.text
                    team_dict[team].append(player)
                    
        df = pd.DataFrame.from_dict(team_dict)
        self.team_lineups = df     
        return df

        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download the current Premier League Soccer data.',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='Example:\n'\
                './collect_epl.py -o ~/Desktop/matchday_17')

    parser.add_argument('-o', '--output', help='Output directory.', required=True, type=str)
    parser.add_argument('-v', '--version', action='version', version='v. 1.0.1')
    
    args = parser.parse_args()

    epl_data = SoccerData()
    epl_data.get_all()
    epl_data.to_csv(args.output)
    
