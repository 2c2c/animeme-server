Backend for a myanimelist.net recommendation engine.

Recommendation engines are a common problem and there are a lot of resources available to implement your own. Example datasets will typically consist of 4-tuples of `userid, itemid, rating, timestamp` (timestamp won't serve any purpose). If you can manage to find or build a dataset with that format, you will have no trouble making a pretty good recommendation engine.

I scraped a large dataset from MAL(they don't have an api) and built a dataset with it. I used a scikit recommendation library and played with SVD and KNN based algorithms. SVD gets results with a standard error of less than one (the ratings will typically be predicting within +-1 from the actual rating on average).
