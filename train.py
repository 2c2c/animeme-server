from surprise import SVD
from surprise import KNNBaseline
from surprise import Dataset
from surprise import evaluate, print_perf
from surprise import Reader
from surprise import dump

from collections import defaultdict
import os
import mal


class Recommendor:
    def train_from_dataset(self, filepath):
        """
        train algorithm from a ratings dataset.

        Use to rebuild a dump of the trained algorithm if it's ever lost
        """
        print("start training")
        # path to dataset file
        file_path = os.path.expanduser(filepath)

        reader = Reader(
            line_format='user item rating timestamp',
            sep=',',
            rating_scale=(1, 10))

        data = Dataset.load_from_file(file_path, reader=reader)

        trainset = data.build_full_trainset()
        # SVD style
        algo = SVD()

        # KNN style
        # sim_options = {'name': 'pearson_baseline', 'user_based': True}
        # algo = KNNBaseline(k=1, min_k=1, sim_options=sim_options)

        algo.train(trainset)

        print("end training")
        self.data = data
        self.algorithm = algo

    def __init__(self):
        _, self.algorithm = self.restore("./reduced_dump")
        self.anime_list = self._anime_list()

    def backup(self, filepath):
        dump.dump(filepath, predictions=None, algo=self.algorithm, verbose=1)

    def restore(self, filepath):
        return dump.load(filepath)

    def _anime_list(self):
        # get unique list of all animes in training data
        print("start animelist")

        anime_list = {}
        with open("./animes", encoding="utf-8") as file_handler:
            lines = file_handler.read().splitlines()

            for line in lines:
                tokens = line.split(",")
                anime_id = tokens[0]
                title = tokens[1]

                # if title is dne, it didn't get its title scraped properly. setting to animeid gives a more useful output
                if title == "dne":
                    anime_list[anime_id] = None
                else:
                    anime_list[anime_id] = title

        print("end animelist")
        return anime_list

    def get_top_n(self, predictions, n=10):
        '''Return the top-N recommendation for each user from a set of predictions.

        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.

        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
        '''

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

    def _test(self, user):
        u = user

        user_animes = [ua[1] for ua in u.ratings]

        # create 3-tuples of userid, animeid, rating.
        # rating is bogus but we need this shape to generate predictions
        target = [(u.ratings[0][0], anime_id, 0)
                  for anime_id in self.anime_list.keys()
                  if anime_id not in user_animes]

        predictions = self.algorithm.test(target)

        return predictions

    def ratings(self, user):
        predictions = self._test(user)
        top_n = self.get_top_n(predictions, n=10)

        ratings = top_n[user.user_id]
        new_ratings = []
        for r in ratings:
            anime_id = r[0]
            rating = r[1]
            #todo null check?
            anime_title = self.anime_list[anime_id]

            new_rating = {
                "animeId": anime_id,
                "title": anime_title,
                "rating": rating,
            }

            new_ratings.append(new_rating)

        #todo map the data in useful format
        # username
        # userid
        # ratings
        #  animename
        #  animeid
        #  animerating

        formatted_data = {
            "username": user.username,
            "userId": user.user_id,
            "ratings": new_ratings
        }

        return dict(formatted_data)


if __name__ == "__main__":
    r = Recommendor()
    # r.train_from_dataset("./reduced_ratings")
    # r.backup("./reduced_dump")
    # _, res = r.restore()
    # print(res)
    u = mal.User("2c2c")
    preds = r.ratings(u)
    print(preds)
