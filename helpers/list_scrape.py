#userid,animeid,rating,timestamp
# http://myanimelist.net/malappinfo.php?u=2c2c
# used to build dataset

import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xmltodict
import urllib3
import time

urllib3.disable_warnings()

headers = {
    "accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding":
    "gzip, deflate, br",
    "accept-language":
    "en-US,en;q=0.8",
    "dnt":
    "1",
    "upgrade-insecure-requests":
    "1",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}




with open('users') as fp:
    with open("ratings", "w") as ratings_file:
        for i, user in enumerate(fp):
            try:
                # omit the newline from file readin
                user = user[:-1]
                print(f"on user {i} {user}")
                time.sleep(1)

                profile_search = f"http://myanimelist.net/malappinfo.php?u={user}"
                r = requests.get(profile_search, headers=headers, verify=False)
                xml = xmltodict.parse(r.text)
                user_id = xml["myanimelist"]["myinfo"]["user_id"]

                for anime in xml["myanimelist"]["anime"]:
                    anime_id = anime["series_animedb_id"]
                    rating = anime["my_score"]
                    genre = anime["series_type"]

                    ratings_file.write(
                        f"{user_id},{anime_id},{rating},{genre}\n")
            except:
                print("exception")
