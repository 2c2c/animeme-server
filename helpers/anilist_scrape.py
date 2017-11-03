# a generate a mapping of all animeids -> animenames
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

with open("./animes", "r") as file_reader:
    with open("./new_animes", "w") as file_writer:
        lines = file_reader.read().splitlines()
        for line in lines:
            tokens = line.split(",")
            anime_id = tokens[0]
            title = tokens[1]

            if title != "dne":
                file_writer.write(f"{line}\n")
                continue

            try:
                print(f"working on animeid {anime_id}")
                anime_url = f"http://jikan.me/api/anime/{anime_id}"

                r = requests.get(anime_url, verify=False)
                time.sleep(.1)
                if r.status_code < 400:
                    data = r.json()
                    anime_title = data["title"]
                    print(anime_title)
                    file_writer.write(f"{anime_id},{anime_title}\n")
                elif r.status_code == 429:
                    sys.exit()
                else:
                    file_writer.write(f"{anime_id},dne\n")

            except (SystemExit):
                print("rate limiting @", line)
                break

            except:
                print(f"threw in {anime_id}")
