# Download Premier League Standings

Sebastian Raschka, 2014

A command line tool to download the current Premier League Soccer standings from [http://www.espnfc.com](http://www.espnfc.com/barclays-premier-league/23/table).

<br>

<hr>
<a id='sections'></a>
### Sections
- [Overview and Examples](#overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Changelog](#changelog)

<hr>

<br>
<br>
<a id='overview'>
## Overview and Examples
[[back to top](#sections)]
<br>
<br>
Running the fantasy soccer data collector from the command line is easy: Just provide a output path for the results (and optionally print the column legend), and you are good to go!

**Example:**

	python epl_standings.py -o ~/Desktop/soccerdata.csv -l

**Output: **

<pre>
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
</pre>

![](./images/example_table.png)

<br>
<br>
<a id='requirements'>
# Requirements
[[back to top](#sections)]

The `Premier League Standings Collector` was built and tested in Python 3 and requires the following external Python packages:

- [BeautifulSoup 4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2)
- [html5lib](https://pypi.python.org/pypi/html5lib)
- [requests](https://pypi.python.org/pypi/requests)
- [pandas](http://pandas.pydata.org)

The packages can be downloaded and installed, e.g., via `pip`

	pip install <package_name>

or

	python -m pip install <package_name>

<br>
<br>
<a id='usage'>
# Usage
[[back to top](#sections)]


<pre>
python epl_standings.py -h
usage: epl_standings.py [-h] -o OUTPUT [-l] [-v]

A command line tool to download the current Premier League Soccerstandings from http://www.espnfc.com/barclays-premier-league/23/table

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output CSV file.
  -l, --legend          Print column legend.
  -v, --version         show program's version number and exit

Example:
./epl_standings.py -o soccerdata.csv</pre>

<br>
<br>
<a id='changelog'>
# Changelog
[[back to top](#sections)]

- v1.0 (12/22/2014)