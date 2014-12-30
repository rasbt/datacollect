# Fantasy Soccer Data Downloader

Sebastian Raschka, 2014

A simple command line tool to download English Premier League (fantasy) soccer data from 

- [https://www.dreamteamfc.com](https://www.dreamteamfc.com/statistics/players/ALL/) (General statistics and fantasy points)
- [http://www.espnfc.com](http://www.espnfc.com/barclays-premier-league/23/table) (Team standings)
- [http://365stats.com](http://365stats.com/football/injuries) (Injuries and suspensions)
- [http://www.transfermarkt.com](http://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1) (Fixtures)
- [https://fantasyfootball.telegraph.co.uk](https://fantasyfootball.telegraph.co.uk/premierleague/players/) (Fantasy points)
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
Running the fantasy soccer data collector from the command line is easy: Just provide a output path for the results, and you are good to go!

**Example:**

	python collect_fantasysoccer.py -o ~/Desktop/soccerdata/

**Output:**

After the script completed, you'll find 5 CSV files with data in the output directory:

![](./images/example_csv.png)


**Screen Output: **

<pre>Getting general statistics from dreamteamfc.com ...
Getting team standings from espnfc.com ...
Getting injury data from 365stats.com ...
Getting home/away data from transfermarkt.com ...
Getting player form data from telegraph.co.uk ...
examples/dreamteamfc_20141230.csv written
examples/espn_20141230.csv written
examples/365stats_20141230.csv written
examples/transfermarkt_20141230.csv written
examples/telegraph_20141230.csv written</pre>

<br>
<br>
<a id='requirements'>
# Requirements
[[back to top](#sections)]

The `Fantasy Soccer Data Collector` was built and tested in Python 3 and requires the following external Python packages:

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
python collect_fantasysoccer.py -h
usage: collect_fantasysoccer.py [-h] -o OUTPUT [-v]

A command line tool to download current Premier League (Fantasy) Soccer data.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory.
  -v, --version         show program's version number and exit

Example:
./collect_fantasysoccer.py -o ~/Desktop/matchday_17</pre>

<br>
<br>
<a id='changelog'>
# Changelog
[[back to top](#sections)]

- v1.0 (12/29/2014)