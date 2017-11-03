# a generate a mapping of all animeids -> animenames
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

with open("./animes", "w") as file_handler:
    for anime_id in range(1, 50000):
        try:
            print(f"working on animeid {anime_id}")
            time.sleep(.5)

            anime_url = f"https://myanimelist.net/anime/{anime_id}"
            r = requests.get(anime_url, verify=False)

            if r.status_code < 400:
                soup = BeautifulSoup(r.text, "html.parser")
                # the name of animes are in the title of the page
                # animename - MyAnimeList.net
                # have to split the latter half
                title_string = soup.find_all(name="title")[0].text.strip()
                pivot_index = title_string.find(" - MyAnimeList.net")
                anime_title = title_string[:pivot_index]
                print(anime_title)
                file_handler.write(f"{anime_id},{anime_title}\n")
            else:
                file_handler.write(f"{anime_id},dne\n")

        except:
            print(f"threw in {anime_id}")
