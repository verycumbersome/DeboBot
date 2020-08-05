import utils
import json
import re
import pandas as pd

import config

def main():
    """Main function loop"""
    data = []

    for screen_name in config.TWITTER_NAMES:
        method = "GET"
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        parameters = {
            "screen_name":screen_name,
            "include_rts":"false",
            "exclude_replies":"true",
            "count":str(config.COUNT),
            }
        timeline = utils.make_call(method, url, parameters)

        for index, item in enumerate(json.loads(timeline.content)):
            text = re.sub(r"http\S+", "", item["text"])
            data.append(text)

    df = pd.DataFrame(data)
    df.to_csv("data/textdata.csv", index=False)

    print(pd.read_csv("data/textdata.csv"))

if __name__ == "__main__":
    main()
