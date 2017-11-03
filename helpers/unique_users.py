# script to output dataset info
def unique_users(filename):
    users = {}
    animes = {}
    with open(filename) as fp:
        for i, line in enumerate(fp):
            (user_id, anime_id, rating, genre) = line.split(",")
            users[user_id] = True
            animes[anime_id] = True

    print(f"ratings: {i}")
    print(f"users: {len(users)}")
    print(f"animes: {len(animes)}")


fn = "ratings"
unique_users(fn)