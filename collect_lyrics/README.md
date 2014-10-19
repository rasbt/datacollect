# Song Lyrics Collector

A simple command line tool to download song lyrics given artist names and song titles. 

<br>

<hr>
<a id='sections'></a>
### Sections
- [Overview and Examples](#overview)
	- [Download lyrics directly from the command line](#download_lyrics_directly_from_the_command_line)
	- [Download a list of lyrics](#download_a_list_of_lyrics)
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

<a id='download_lyrics_directly_from_the_command_line'>
### Download lyrics directly from the command line
[[back to top](#sections)]
<pre>
./collectlyrics.py -a "Bob Dylan" -t "blowing in the wind"

How many roads must a man walk down
Before you call him a man?
How many seas must the white dove sail
Before she sleeps in the sand?

[...]
The answer is blowin' in the wind
</pre>

<br>
<br>

<a id='download_a_list_of_lyrics'>
### Download a list of lyrics:
[[back to top](#sections)]

Or you can directly read a list of artists and titles from a CSV file. The input CSV file should be formatted as follows:

	Artist,Title
	Bob Dylan,blowing in the wind
	U2,Iris (hold me close)
	Badfinger,Baby blue
	Red hot chili peppers,by the way

A progress bar ([`pyprind`](https://github.com/rasbt/pyprind)) will show the progress during the download process. 

	> ./collectlyrics.py -i ./examples/artist_title.csv -o out.csv
	0%  100%
	[####] | ETA[sec]: 0.144 
	Total time elapsed: 0.540 sec

And the output CSV file will look as follows (here shown as screenshot using a spread sheet application, Numbers):

![](./images/example_out.png)

<br>
<br>
<a id='requirements'>
# Requirements
[[back to top](#sections)]

The `Lyrics Collector` was built and tested in Python 3 and requires the following external Python packages:

- [lxml.html](http://lxml.de/lxmlhtml.html)
- [pandas](http://pandas.pydata.org)
- [pyprind](https://github.com/rasbt/pyprind)

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
./collectlyrics.py --help
usage: collectlyrics.py [-h] [-a ARTIST] [-t TITLE] [-i INPUT] [-o OUTPUT]
                        [-v]

A command line tool to download song lyrics from LyricWikia.com

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Artist name.
  -t TITLE, --title TITLE
                        Song title.
  -i INPUT, --input INPUT
                        Input CSV file.
  -o OUTPUT, --output OUTPUT
                        Output CSV file.
  -v, --version         show program's version number and exit

Example:
./collectlyrics.py -a "Bob Dylan" -t "blowing in the wind"

./collectlyrics.py -i ./input.csv -o ./output.csv

CSV input format:

Artist,Title
Bob Dylan,blowing in the wind
[...]
</pre>

<br>
<br>
<a id='changelog'>
# Changelog
[[back to top](#sections)]

- v1.0 (10/18/2014)