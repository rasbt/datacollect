#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Tested in Python 3

# Sebastian Raschka, 2014
# An interactive command line app for
# creating a PDB file info table.
# For help, execute
# ./pdb_infotable.py --help

import bs4
import urllib
import pyprind
import pandas as pd

class Pdb(object):
    def __init__(self, pdb_code):
        self.code = pdb_code.strip().lower()
        self.reso = None
        self.desc = '-'
        self.titl = None
        self.ligs = {}
        self.meth = None
        self.soup = None
        self.cont = None
        
    def lookup(self):
        self.soup = self.__get_soup()
        self.__get_resolution()
        self.__get_title()
        self.__get_description()
        self.__get_pdbcontent()
        self.__get_ligands()
        
    def get_summary(self):
        self.lookup()
        summary = [self.code, self.desc, self.reso, self.meth, self.ligs, self.titl]
        return summary
        
    def __get_soup(self):
        url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + self.code
        return bs4.BeautifulSoup(urllib.request.urlopen(url))
    
    def __get_pdbcontent(self):
        url = 'http://www.rcsb.org/pdb/files/' + self.code + '.pdb'
        r = urllib.request.urlopen(url)
        self.cont = r.readlines()
    
    def __get_resolution(self):
        try:
            reso_tag = self.soup.find('td', {'id': 'se_xrayResolution'})
            resolution = reso_tag.contents[0].strip()
            self.meth = 'X-Ray'
            self.reso = resolution
        except AttributeError:
            self.meth = 'NMR'
            self.reso = '-'
    
    def __get_title(self):
        try:
            parent = self.soup.find('div', {'id': 'se_structureTitle'})
            child = parent.find('span', {'class': 'h3'})
            title = child.contents[0]
            self.titl = title
        except AttributeError:
            self.titl = '-'
    
    def __get_description(self):
        try:
            desc_tag = self.soup.find('td', {'class': 'mdauData', 'colspan':"99"})
            description = desc_tag.contents[0].strip()
            self.desc = description
        except AttributeError:
            self.desc = '-'      
    
    def __get_ligands(self):
        for i in self.cont:
            i = i.decode('utf-8')
            if i.startswith('HETNAM'):
                s = i.split('HETNAM')[1].strip()
                sp = s.split()
                short = sp[0]
                if len(short) == 1:
                    short = sp[1]
                    desc = " ".join(sp[2:])
                else:
                    desc = " ".join(sp[1:])
                
                if short in self.ligs:
                    self.ligs[short] += desc
                else:
                    self.ligs[short] = desc

        
def make_table(csv_in, csv_out):
    df = pd.read_csv(csv_in, sep=',', header=None)
    df.columns = ['PDB']
    
    progress_bar = False
    if df.shape[0] > 3:
        progress_bar = pyprind.ProgBar(df.shape[0])
    
    descs = []
    resolutions = []
    methods = []
    ligands_short = []
    ligands_long = []
    titles = []
    
    for row in df.index:
        new_pdb = Pdb(df.loc[row]['PDB'])
        new_pdb.lookup()
        descs.append(new_pdb.desc.lower())
        resolutions.append(new_pdb.reso)
        methods.append(new_pdb.meth)
        ligands_short.append('; '.join(new_pdb.ligs.keys()))
        ligands_long.append('; '.join(new_pdb.ligs.values()))
        titles.append(new_pdb.titl)
        
        if progress_bar:
            progress_bar.update()
    #df.to_csv(csv_out)
    df['Description'] = pd.Series(descs, df.index)
    df['Resolution (A)'] = pd.Series(resolutions, df.index)
    df['Method'] = pd.Series(methods, df.index)
    df['Title'] = pd.Series(titles, df.index)
    df['Ligands (short)'] = pd.Series(ligands_short, df.index)
    df['Ligands (long)'] = pd.Series(ligands_long, df.index)
    df.to_csv(csv_out)
    

        
    
if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool for creating a PDB file info table.',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='\nExample run:\n'\
                './pdb_infotable.py -i pdb_codes.txt -o ./pdb_table.csv\n\n'\
                'Example input file:\n'\
                '1htg\n3eiy\n1hvr\n[...]')

    parser.add_argument('-i', '--input', help='A 1-column text file with PDB codes.')
    parser.add_argument('-o', '--output', help='Filename for creating the output CSV file.')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')
    
    args = parser.parse_args()

    
    if not args.output:
        print('Please provide a filename for creating the output CSV file.')
        quit()
        
    if not args.input:
        print('Please provide a file for the PDB codes.')
        quit()
    
    make_table(args.input, args.output)
    
