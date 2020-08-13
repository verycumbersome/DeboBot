"""Engine for the twitter scraper and model text generation"""
import sys
import json
import re
import datetime
import pandas as pd
# import gpt_2_simple as gpt2
import tqdm

import config
import utils


def make_status_update(status):
    """Function to make a status update"""
    method = "POST"
    url = "https://api.twitter.com/1.1/statuses/update.json"
    parameters = {
            "status":status,
        }
    print("Making post \'" + status + "\'")
    timeline = utils.make_call(method, url, parameters)


def get_timeline(screen_name, depth):
    """Function to return values from a user's timeline"""
    max_id = 0
    data = []
    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    print("Scraping tweets from \'" + screen_name + "\'")
    for _ in tqdm.tqdm(range(depth)):
        parameters = {
            "max_id": max_id - 1,
            "screen_name": screen_name,
            "include_rts": "false",
            "exclude_replies": "true",
            "tweet_mode": "extended",
            "count": str(config.SCRAPE_TIMELINE_COUNT),
            }

        if not max_id:
            parameters.pop("max_id")

        timeline = utils.make_call(method, url, parameters)

        if timeline.status_code == 200:
            for item in json.loads(timeline.content):
                max_id = item["id"]
                text = re.sub(r"http\S+", "", item["full_text"])
                data.append(text)

    return data


def error(msg):
    """Error function for program"""
    print("ERROR:", msg)
    exit()


def main():
    """Main function"""
    for index, arg in enumerate(sys.argv):
        if arg == "--scrape":
            try:
                data = {"text": []}

                for screen_name in config.TWITTER_NAMES:
                    data["text"].extend(get_timeline(
                        screen_name, config.SCRAPE_DEPTH))

                df = pd.DataFrame(data=data)
                df.to_csv("data/textdata.csv", index=False)

            except Exception:
                error("Must enter scrape depth and length")

        if arg == "--txt":
            utils.convert_to_txt("data/textdata.csv")

        if arg == "--gen":
            sess = gpt2.start_tf_sess()
            gpt2.load_gpt2(sess, run_name='run1')

            gen_file = "gpt2_gentext_{:%Y%m%d_%H%M%S}.txt".format(datetime.datetime.utcnow())

            gpt2.generate_to_file(
                sess,
                destination_path=gen_file,
                length=500,
                temperature=0.7,
                nsamples=100,
                batch_size=20
                )

        if arg == "--post":
            tweet = utils.get_random_tweet()

            make_status_update(tweet)

if __name__ == "__main__":
    main()
