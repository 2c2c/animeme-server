# a generate a mapping of all animeids -> animenames
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

with open("./animes", "r", encoding="utf-8") as file_reader:
    with open("./new_animes", "w", encoding="utf-8") as file_writer:
        lines = file_reader.read().splitlines()

        old_lines = lines[:16481]
        for line in old_lines:
            file_writer.write(f"{line}\n")

        lines = lines[16481:]
        for line in lines:
            tokens = line.split(",")
            anime_id = tokens[0]
            title = tokens[1]

            if title != "dne":
                file_writer.write(f"{line}\n")
                continue

            try:
                print(f"working on animeid {anime_id}")
                anime_url = f"https://myanimelist.net/anime/{anime_id}"
                # manga_url = f"https://myanimelist.net/manga/{anime_id}"
                status = 500
                count = 0
                while status > 400 and count < 3:
                    print("attempt", count)
                    time.sleep(.8)
                    # r = requests.get(manga_url, verify=False)
                    r = requests.get(anime_url, verify=False)
                    status = r.status_code
                    print(r.status_code)
                    count += 1

                if r.status_code < 400:
                    soup = BeautifulSoup(r.text, "html.parser")
                    # the name of animes are in the title of the page
                    # animename - MyAnimeList.net
                    # have to split the latter half
                    title_string = soup.find_all(name="title")[0].text.strip()
                    pivot_index = title_string.find(" - MyAnimeList.net")
                    anime_title = title_string[:pivot_index]
                    print(anime_title)
                    file_writer.write(f"{anime_id},{anime_title}\n")
                else:
                    file_writer.write(f"{anime_id},dne\n")

            except Exception as exc:
                print(f"threw in {anime_id}")
                print(exc.args)
