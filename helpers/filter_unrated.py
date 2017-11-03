#0 rated items are ruining results, quick script 2 fix
def filter_unrated(filename, filename2):
    users = {}
    animes = {}
    with open(filename) as fp:
        with open(filename2, "w") as fp2:
            for i, line in enumerate(fp):
                (user_id, anime_id, rating, genre) = line.split(",")
                
                if rating != "0":
                    fp2.write(line)


filter_unrated("ratings", "new_ratings")