# scrape mal club section for users
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

def write_users(ulist):
    with open("./users", 'w') as file_handler:
        for item in ulist:
            file_handler.write("{}\n".format(item))

userlist = set([])
for club_id in range(1, 15000):
    try: 
        print(f"working on clubid {club_id}")
        print(f"set length: {len(userlist)}")

        if club_id % 1000 == 0:
            write_users(userlist)

        # show is query parameter for pagination, incr by 36
        show = 0
        time.sleep(1)

        club_url = "https://myanimelist.net/clubs.php?action=view&t=members"
        club_url += f"&id={club_id}"
        r = requests.get(club_url, verify=False)

        while r.status_code < 400:
            print(f"working on show {show}")
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all(name="a", href=True)
            for item in items:
                # print(item["href"])
                p = re.compile("^\/profile\/(.*)")
                m = p.match(item["href"])
                if m is not None:
                    # print(m.group(1))
                    user = m.group(1)
                    userlist.add(user)
            time.sleep(.5)
            show += 36
            paginated_url = club_url + f"&show={show}"
            r = requests.get(paginated_url, verify=False)
    except:
        print(f"threw in {club_id}")
