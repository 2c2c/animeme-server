import train
import mal

from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

# train the dataset and leave it in memory
# this blocks hard. use small dataset when developing
r = train.Recommendor()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/recommendations")
def ratings():
    username = request.args.get("username")
    u = mal.User(username)
    recommendations = r.ratings(u)
    return jsonify(recommendations)
