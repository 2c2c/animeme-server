#userid,animeid,rating,timestamp
# http://myanimelist.net/malappinfo.php?u=2c2c
#extract userid
#extract each animeid and rating

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

class User:
    def __init__(self, username):
        self.anime_mapping = dict()
        profile_search = f"http://myanimelist.net/malappinfo.php?u={username}&status=all"
        r = requests.get(profile_search, headers=headers, verify=False)

        xml = xmltodict.parse(r.text)
        user_id = xml["myanimelist"]["myinfo"]["user_id"]

        ratings = []
        for anime in xml["myanimelist"]["anime"]:
            anime_id = anime["series_animedb_id"]
            title = anime["series_title"]
            rating = anime["my_score"]
            genre = anime["series_type"]

            self.anime_mapping[anime_id] = title
            ratings.append((user_id, anime_id, rating, title, genre))

        self.ratings = ratings
        self.username = username
        self.user_id = user_id

    def ratings_triple(self):
        """
        return 3-tuple typically used in recommendation engines

        userid,itemid,rating
        """
        target = self.ratings
        target = filter(lambda x: x[2] != "0", target)
        target = [(x[0], x[1], int(x[2])) for x in target]

        return target


def parse_ratings(username):
    profile_search = f"http://myanimelist.net/malappinfo.php?u={username}&status=all"
    r = requests.get(profile_search, headers=headers, verify=False)
    xml = xmltodict.parse(r.text)
    user_id = xml["myanimelist"]["myinfo"]["user_id"]

    ratings = []
    for anime in xml["myanimelist"]["anime"]:
        anime_id = anime["series_animedb_id"]
        title = anime["series_title"]
        rating = anime["my_score"]
        genre = anime["series_type"]

        ratings.append((user_id, anime_id, rating, title, genre))

    return ratings


if __name__ == "__main__":
    u = User("2c2c")
    target = u.ratings_triple()

    print(target)