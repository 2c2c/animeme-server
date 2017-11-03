# a generate a mapping of all animeids -> animenames
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

count = 0
with open("./animes", "r", encoding="utf-8") as file_reader:
    lines = file_reader.read().splitlines()
    for line in lines:
        tokens = line.split(",")
        anime_id = tokens[0]
        title = tokens[1]

        if title != "dne":
            count += 1

print("animes", count)
count = 0
with open("./new_animes", "r", encoding="utf-8") as file_reader:
    lines = file_reader.read().splitlines()
    for line in lines:
        tokens = line.split(",")
        anime_id = tokens[0]
        title = tokens[1]

        if title != "dne":
            count += 1

print("new animes", count)