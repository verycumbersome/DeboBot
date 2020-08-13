import os
import random
import pandas as pd
from flask import Flask

import engine

app = Flask(__name__)


@app.route("/")
def home_view():
    # Gets a random tweet from 
    tweet = get_random_tweet()

    engine.make_status_update(tweet)

    return "<h1>" + tweet + "</h1>"


if __name__ == "__main__":
    engine.make_status_update("hi!")
    app.run()
