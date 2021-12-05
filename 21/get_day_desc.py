#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [day number]")
    quit()

day = sys.argv[1]
if int(day) not in range(1, 32):
    print(f"Usage: {sys.argv[0]} [day_number]")
    quit()

url = "https://adventofcode.com/2021/day/"
res = requests.get(url + day)
if (res.status_code != 200):
    print(f"Bad HTTP response: {res.status}. Exiting...")
    quit()

soup = BeautifulSoup(res.content, 'html.parser')
article = soup.find_all('article')

if not article:
    print(f"ERROR: tried to parse {url}{day} but didn't find 'article' tag. Exiting...")

print(article)
