# PDB Info table

A simple command line tool that creates an info table from a list of PDB files.

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

An input file is just a simple 1-column text file of PDB codes, e.g., 

	3eiy
	1htg
	1amu
	1hvr

By executing the following line, all PDB codes from an input file `test.csv` are queried and the information that could be retrieved is saved to the output file `test_out.csv`.


	./pdb_infotable.py -i ./examples/test.csv -o ./examples/test_out.csv
	0%             100%
	[############  ] | ETA[sec]: 5.762


![](./images/example.png)

<br>
<br>
<br>
<br>
<a id='requirements'>
## Requirements
[[back to top](#sections)]


The ` PDB Info Table` tool was built and tested in Python 3 and requires the following external Python packages:

- [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
- [pandas](http://pandas.pydata.org)
- [pyprind](https://github.com/rasbt/pyprind)

The packages can be downloaded and installed, e.g., via `pip`

	pip install <package_name>

or

	python -m pip install <package_name>

<br>
<br>
<a id='usage'>
## Usage
[[back to top](#sections)]


<pre>
./pdb_infotable.py -h
usage: pdb_infotable.py [-h] [-i INPUT] [-o OUTPUT] [-v]

A command line tool for creating a PDB file info table.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        A 1-column text file with PDB codes.
  -o OUTPUT, --output OUTPUT
                        Filename for creating the output CSV file.
  -v, --version         show program's version number and exit

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

- v1.0 (10/19/2014)