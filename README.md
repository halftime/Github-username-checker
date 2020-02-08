# Github username checker

Multithreaded github username checker

## Examples found:

![example found github](https://i.imgur.com/598ipUA.png)

## Prerequisites

* Python 3
* Python requests library (pip install requests)
* Wordlist (e.g: rockyou.txt)

## Running

usage: github_checker.py [-h] wordlist threads

Find 404'd (untaken) github profiles

positional arguments:
* wordlist    Wordlist to read usernames from (wordlist.txt)
* threads     Amount of threads (24)

optional arguments:
  -h, --help  show this help message and exit

### Command line example

python github_checker.py "rockyou.txt" 24

## Note 

* See sample output: found-top10k.txt
* Script will check for profiles that return 404 status code.
* Manual confirmation is still required, further down sorted wordlist = more likely to be untaken
