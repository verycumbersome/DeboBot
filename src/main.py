import os
import random
import pandas as pd
from flask import Flask

import utils
import engine

app = Flask(__name__)


@app.route("/")
def home_view():
    tweets = []
    text_path = "../text/"
    for file in os.listdir(text_path):
        with open(text_path + file, "r") as fp:
            tweets.extend(fp.read().split("<|startoftext|>"))
    # Remove duplicates and exd of text
    tweets = list(set([tweet.replace("<|endoftext|>", "") for tweet in tweets]))

    # Select a random tweet from the options
    tweet = random.choice(tweets)

    # Checks if the generated tweets is in the orignal dataset
    training = pd.read_csv("../src/data/textdata.csv")
    while ([True for item in training["text"] if str(tweet).lower() == str(item).lower()]):
        print("UNORIGINAL TWEET:", tweet)
        tweet = random.choice(tweets)

    engine.make_status_update(tweet)

    return "<h1>" + tweet + "</h1>"


if __name__ == "__main__":
    app.run()
