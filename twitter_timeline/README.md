# Twitter Timeline Downloader

A simple command line tool that downloads your personal twitter timeline in CSV format with optional keyword filter.

<br>

<hr>
<a id='sections'></a>
### Sections
- [Example](#example)
- [Setup](#setup)
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

By executing the following line, we download all timeline tweets that contain the keyword `Python` (case-insensitive) and save them to a CSV file `python_tweets.csv`. The `tweets downloaded` indicates the progress during the execution, you can always abort the script by pressing `CTRL+C`.

	./twitter_timeline.py -o python_tweets.csv -k Python
	Authentification successful: True
	tweets downloaded: 1200


![](./images/python_tweets.png)

<br>
<br>
<a id='setup'>
## Setup
[[back to top](#sections)]

In order to get access to the Twitter API through OAuth (open standard for authorization), we have to obtain our consumer information and access tokens first by registering our app on [https://apps.twitter.com](https://apps.twitter.com).

1. Click on the "Create New App" button and fill out the information  
2. Obtain the Consumer key, Consumer secret, Access token, and Access token secret.



![OAuth settings](./images/oauth_settings.png)
PLEASE DON'T SHARE THIS INFORMATION WITH OTHER USERS ON THE INTERNET!

Next to the `twitter_timeline.py` script, you can find a `oauth_info.py` file. Please fill in the information you retrieved from the [https://apps.twitter.com](https://apps.twitter.com) website (and remember to keep this file private!).

This is it, `twitter_timeline.py` is now good to go!

<br>



	CONSUMER_KEY = 'enter your information here'
	CONSUMER_SECRET = 'enter your information here'
	ACCESS_TOKEN = 'enter your information here'
	ACCESS_TOKEN_SECRET = 'enter your information here'
	USER_NAME = 'enter your twitter handle here'




<br>
<br>
<a id='requirements'>
## Requirements
[[back to top](#sections)]


The ` Twitter Timeline Downloader` was built and tested in Python 3 and requires the following external Python packages:

- [twitter](https://pypi.python.org/pypi/twitter/1.15.0)
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
./twitter_timeline.py --help
usage: twitter_timeline.py [-h] [-o OUT] [-m MAX] [-k KEYWORDS] [-v]

A command line tool to download your personal twitter timeline.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     Filename for creating the output CSV file.
  -m MAX, --max MAX     Maximum number (integer) of timeline tweets query (searches all by default)
  -k KEYWORDS, --keywords KEYWORDS
                        A comma separated list of keywords  for filtering (optional).
  -v, --version         show program's version number and exit

Example:
./twitter_timeline.py -o my_timeline.csv -k Python,Github</pre>

<br>
<br>
<a id='changelog'>
## Changelog
[[back to top](#sections)]

- v1.0 (10/19/2014)