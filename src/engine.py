"""Engine for the twitter scraper and model text generation"""
import os
import sys
import json
import re
import datetime
import pandas as pd
# import gpt_2_simple as gpt2
import tqdm

import config
import utils

file_dir = os.path.dirname(__file__)


def delete_tweet(tweet_id):
    """Function to delete a post"""
    method = "POST"
    url = "https://api.twitter.com/1.1/statuses/destroy/" + str(tweet_id) + ".json"
    parameters = {
            "id":tweet_id,
        }
    print("Deleting tweet \'" + str(tweet_id) + "\'")
    return utils.make_call(method, url, parameters)


def make_status_update(status):
    """Function to make a status update"""
    method = "POST"
    url = "https://api.twitter.com/1.1/statuses/update.json"
    parameters = {
            "status":status,
        }
    print("Making post \'" + status + "\'")
    return utils.make_call(method, url, parameters)


def get_rate_limit():
    """Function to make a status update"""
    method = "GET"
    url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
    parameters = {}
    return json.loads(utils.make_call(method, url, parameters).content)



def get_timeline(screen_name, depth, prune_tweets=False):
    """Function to return values from a user's timeline"""
    max_id = 0
    data = []
    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    # print("Scraping tweets from \'" + screen_name + "\'")
    for _ in tqdm.tqdm(range(depth), desc=screen_name):
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

        while(True):
            # If the response code is "Ok" let the iteration keep going
            if timeline.status_code == 200:
                for item in json.loads(timeline.content):
                    max_id = item["id"]
                    text = re.sub(r"http\S+", "", item["full_text"])
                    data.append(text)

                    if prune_tweets and item["favorite_count"] < 1:
                        delete_tweet(item["id"])
                break

            # If the response code is not "Ok" remain looping
            else:
                time.sleep(3)
                pass


    return data


def error(msg):
    """Error function for program"""
    print("ERROR:", msg)
    exit()


def main():
    """Main function"""
    for index, arg in enumerate(sys.argv):
        # Scrape the tweets from all users in the TWITTER_NAMES array in config
        if arg == "--scrape":
            try:
                data = {"text": []}

                for screen_name in config.TWITTER_NAMES:
                    data["text"].extend(get_timeline(
                        screen_name, config.SCRAPE_DEPTH))


                file_name = "textdata{:%Y%m%d_%H%M%S}.csv".format(datetime.datetime.utcnow())
                csv_path = os.path.join(file_dir, "data/" + file_name)

                df = pd.DataFrame(data=data)
                df.to_csv(csv_path, index=False)

            except Exception:
                error("Must enter scrape depth and length")

        # Convert all csv files from the scraped data to an output text file for tuning
        if arg == "--txt":
            textdata_path = os.path.join(file_dir, "data/textdata.csv")
            utils.csv_to_txt(textdata_path)

        # Generate a tweet given a GPT2 finetuned model
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

        # Make a post from a randomly selected tweet
        if arg == "--post":
            tweet = utils.get_random_tweet()
            make_status_update(tweet)

        # Remove all posts from the bot's timeline with 0 favorites
        if arg == "--clean":
            timeline = get_timeline("peepeemann", 2, True)

        if arg == "--rate":
            print(json.dumps(get_rate_limit()["resources"]["statuses"], indent=4))


if __name__ == "__main__":
    main()
