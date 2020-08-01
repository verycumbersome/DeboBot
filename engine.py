import os
import requests

import engine
import utils

def main():
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")

    ntp_time = utils.get_ntp_time()
    nonce = utils.get_nonce(32)

    token = utils.get_token()
    print(token)
    # signature = utils.get_signature(
            # True,
            # consumer_key,
            # nonce,
            # "HMAC-SHA1",
            # ntp_time,

            # )

    # url = "https://api.twitter.com/oauth/request_token"
    # headers = {
            # "oauth_consumer_key":consumer_key,
            # "oauth_nonce":nonce,
            # "oauth_signature":,
            # "oauth_signature_method":,
            # "oauth_timestamp":,
            # "oauth_token":,
            # "oauth_version":,
            # }
    # timeline = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2")
    # print(timeline.headers)

if __name__=="__main__":
    main()
