"""Main for hosting webpage"""
import os
import random
import pandas as pd
from flask import Flask

import utils
import engine

app = Flask(__name__)


@app.route("/")
def home_view():
    # Gets a random tweet from the generated tweets
    tweet = utils.get_random_tweet()

    return "<h1>" + tweet + "</h1>"


if __name__ == "__main__":
    app.run()
