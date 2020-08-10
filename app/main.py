import random
import pandas as pd
from flask import Flask

# import src.utils

app = Flask(__name__)

@app.route("/")
def home_view():
    with open("../gpt2_gentext_20200810_015757.txt", "r") as file:
        tweets = file.read().split("<|startoftext|>")
        tweets = list(set([tweet.replace("<|endoftext|>", "") for tweet in tweets]))

    tweet = random.choice(tweets)

    training = pd.read_csv("../src/data/textdata.csv")

    while ([True for item in training["text"] if tweet == item]):
        print("UNORIGINAL TWEET:", tweet)
        tweet = random.choice(tweets)

    return "<h1>" + tweet + "</h1>"


if __name__ == "__main__":
    app.run()

