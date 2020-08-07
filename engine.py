import utils
import json
import re
import pandas as pd
import tqdm

import config

def get_timeline(screen_name, depth):
    """Function to return values from a user's timeline"""
    data = []
    max_id = 0
    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    for i in range(depth):
        parameters = {
            "max_id":max_id,
            "screen_name":screen_name,
            "include_rts":"false",
            "exclude_replies":"true",
            "count":str(config.COUNT),
            }
        if not max_id: parameters.pop("max_id")

        timeline = utils.make_call(method, url, parameters)

        print(json.loads(timeline.content))
        for item in json.loads(timeline.content):
            # print(item)
            max_id = item["id"]
            text = re.sub(r"http\S+", "", item["text"])
            data.append(text)

    return data

def main():
    """Main function"""
    data = []

    # timeline = get_timeline("killmefam", 5)
    # print(len(timeline))

    for screen_name in tqdm.tqdm(config.TWITTER_NAMES):
        data.append(get_timeline(screen_name, 2))

    df = pd.DataFrame(data)
    df.to_csv("data/textdata.csv", index=False)

    # print(pd.read_csv("data/textdata.csv"))

if __name__ == "__main__":
    main()
