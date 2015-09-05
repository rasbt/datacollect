#!/usr/bin/env python

# Sebastian Raschka, 2015
# http://sebastianraschka.com

import bs4
import urllib
import pyprind
import os
import sys

kind_dict = {'.mol2': 'MOL2',
             '.sdf': 'SDF',
             '.ddb': 'Flexibase',
             '.smi': 'SMILES'}

if (sys.version_info > (3, 0)):
     # Python 3 code in this block
     from urllib.request import urlopen
else:
     # Python 2 code in this block
     from urllib import urlopen

def txt_to_ids(id_file):
    with open(id_file, 'r') as f:
        ids = [i.strip() for i in f if i.strip()]
    return ids


def download_zinc_mol(zinc_id, ext):
    kind = kind_dict[ext]
    zinc_id = zinc_id.lower().split('ZINC')[0].lstrip('0')
    url = 'http://zinc.docking.org/substance/' + zinc_id
    soup = bs4.BeautifulSoup(urlopen(url), "lxml")
    res = soup.find('a', {'title': 'Download %s File' % kind}, href=True)
    response = urlopen(res['href'])
    html = response.read().decode('UTF-8')
    return html


def get_filetype(kind):
    if kind == 'mol2':
        kind = '.mol2'
    elif kind == 'smiles':
        kind = '.smi'
    elif kind == 'sdf':
        kind = '.sdf'
    elif kind == 'flexibase':
        kind = '.ddb'
    else:
        raise AttributeError("Invalid filetype")
    return kind


def zinc2onefile(zinc_ids, outfile, kind='mol2'):
    kind = get_filetype(kind)
    bar = pyprind.ProgBar(len(zinc_ids), title='Downloading ZINC Molecules')
    with open(outfile, 'w') as out:
        for m in zinc_ids:
            data = download_zinc_mol(m, kind)
            out.write(data)
            bar.update(item_id=m)


def zinc2files(zinc_ids, outdir, kind='mol2'):
    kind = get_filetype(kind)
    bar = pyprind.ProgBar(len(zinc_ids), title='Downloading ZINC Molecules')
    if not os.path.exists(outdir):
            os.makedirs(outdir)
    for m in zinc_ids:
        zinc_file = m + kind
        zinc_file = os.path.join(outdir, zinc_file)
        bar.update(item_id=m)
        data = download_zinc_mol(m, kind)
        with open(zinc_file, 'w') as out:
            out.write(data)

if __name__ == "__main__":

    kind_allowed = {'mol2', 'sdf', 'flexibase', 'smiles'}
    import argparse

    parser = argparse.ArgumentParser(
            description='A command line tool for downloading 3D structures'
                        ' of small chemical molecules from http://zinc.docking.org.',
            formatter_class=argparse.RawTextHelpFormatter,
            epilog='\nExample run:\n'
                   './zinc_downloader.py -i ./examples/ids.txt -o'
                   ' ./examples/1file.mol2\n\n'
                   'Example input file:\n'
                   'ZINC08714378\nZINC59339553\nZINC67643437\n[...]')

    parser.add_argument('-i', '--input',
                        type=str,
                        help='One-column text file with ZINC codes')
    parser.add_argument('-o', '--output_file',
                        type=str,
                        help='Filename for creating a single output file')
    parser.add_argument('-d', '--output_dir',
                        type=str,
                        help='Directory name for saving multiple output files')
    parser.add_argument('-f', '--filetype',
                        type=str,
                        default='mol2',
                        help='Filetype %s, default=mol2' % kind_allowed)
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    if not (args.output_file or args.output_dir):
        parser.print_help()
        print('\nPlease provide either an output file or output directory.')
        quit()

    if not args.input:
        parser.print_help()
        print('\nPlease provide an iput file for the ZINC codes.')
        quit()

    kind = args.filetype.lower()
    if kind not in kind_allowed:
        parser.print_help()
        print('\nPlease provide an iput file for the ZINC codes.')
        quit()

    zinc_ids = txt_to_ids(args.input)
    if args.output_file:
        zinc2onefile(zinc_ids, args.output_file, kind=kind)
    else:
        zinc2files(zinc_ids, args.output_dir, kind=kind)
