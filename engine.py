import sys
import json
import re
import pandas as pd
import tqdm
import torch
import re
import numpy as np
import tensorflow as tf
import gpt_2_simple as gpt2
import os
import requests

import config
import utils


def get_timeline(screen_name, depth):
    """Function to return values from a user's timeline"""
    max_id = 0
    data = []
    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    print("Scraping tweets from \'" + screen_name + "\'")
    for i in tqdm.tqdm(range(depth)):
        parameters = {
                "max_id":max_id - 1,
                "screen_name":screen_name,
                "include_rts":"false",
                "exclude_replies":"true",
                "tweet_mode":"extended",
                "count":str(config.SCRAPE_TIMELINE_COUNT),
                }
        if not max_id: parameters.pop("max_id")

        timeline = utils.make_call(method, url, parameters)

        if (timeline.status_code == 200):
            for item in json.loads(timeline.content):
                max_id = item["id"]
                text = re.sub(r"http\S+", "", item["full_text"]) + "<eos>"
                data.append(text)

        else:
            print(timeline.content, end="\r")

    return data

def main():
    """Main function"""
    if "--scrape" in sys.argv:
        data = {"text":[]}

        for screen_name in config.TWITTER_NAMES:
            data["text"].extend(get_timeline(screen_name, config.SCRAPE_DEPTH))

        df = pd.DataFrame(data=data)
        df.to_csv("data/textdata.csv", index=False)

    if "--txt" in sys.argv:
        utils.convert_to_txt("data/textdata.csv")

    if "--gen" in sys.argv:
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name='run1')

        while(True):
            text = gpt2.generate(sess,
                    length=250,
                    temperature=0.7,
                    prefix=input("Enter prefix:"),
                    nsamples=1,
                    batch_size=1
                    )

            print(text)

if __name__ == "__main__":
    main()
