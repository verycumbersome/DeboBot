import random
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home_view():
    with open("../gpt2_gentext_20200810_015757.txt", "r") as file:
        tweets = file.read().split("<|startoftext|>")
        tweets = list(set([tweet.replace("<|endoftext|>", "") for tweet in tweets]))

        return "<h1>" + random.choice(tweets) + "</h1>"


if __name__ == "__main__":
    app.run()

