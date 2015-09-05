[Sebastian Raschka](http://sebastianraschka.com)

# ZINC Molecule Downloader

A command line tool for downloading 3D structures of small chemical molecules from http://zinc.docking.org.

![](./images/example-1.png)

<br>

<hr>
<a id='sections'></a>

### Sections
- [Example](#example)
- [Requirements](#requirements)
- [Usage](#usage)
- [Changelog](#changelog)

<hr>

<br>
<br>
<a id='example'>

## Example
[[back to top](#sections)]
<br>
<br>

An input file is just a simple 1-column text file of ZINC codes, e.g.,

	ZINC08714378
	ZINC59339553
	ZINC67643437
	ZINC05481096

By executing the following line, all ZINC codes from an input file `ids.txt` are queried and
the molecular structures are downloaded as individual files or a multi-structure file.
For example, a single multi-structure SDF file is created by executing the following code:


	> python zinc_downloader.py -i ./ids.txt -o ./zinc.sdf --filetype sdf


	Downloading ZINC Molecules
    0%               100%
    [####               ] | ETA[sec]: 31.431 | Item ID: ZINC54810967

<br>
<br>
<br>
<br>
<a id='requirements'>

## Requirements
[[back to top](#sections)]


The ` PDB Info Table` tool was tested in Python 3.4 and Python 2.7. The required packages

    beautifulsoup4>=4.4.0
    lxml>=3.4.4
    PyPrind>=2.9.3


  can be downloaded and installed via `pip`

	pip install -r requirements.txt

<br>
<br>
<a id='usage'>

## Usage
[[back to top](#sections)]


<pre>
> python zinc_downloader.py -h
usage: zinc_downloader.py [-h] [-i INPUT] [-o OUTPUT_FILE] [-d OUTPUT_DIR]
                          [-f FILETYPE] [-v]

A command line tool for downloading 3D structures of small chemical molecules from http://zinc.docking.org.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        One-column text file with ZINC codes
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Filename for creating a single output file
  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory name for saving multiple output files
  -f FILETYPE, --filetype FILETYPE
                        Filetype set(['smiles', 'sdf', 'flexibase', 'mol2']), default=mol2
  -v, --version         show program's version number and exit

Example run:
./zinc_downloader.py -i ./examples/ids.txt -o ./examples/1file.mol2

Example input file:
ZINC08714378
ZINC59339553
ZINC67643437
[...]
(py27)w

Example run:
./pdb_infotable.py -i pdb_codes.txt -o ./pdb_table.csv

Example input file:
1htg
3eiy
1hvr
[...]</pre>

<br>
<br>
<a id='changelog'>

## Changelog
[[back to top](#sections)]

- v1.0 2015-09-05
