import utils
import json
import re
import pandas as pd

def main():
    """Main function loop"""
    twitter_names = [
            "killmefam",
            "darth_erogenous",
            "adda_boi",
            "poop420guy69",
            "toomuchprotein",
            "inclcore",
            "rockanrollphoto"
        ]

    data = []

    for screen_name in twitter_names:
        method = "GET"
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        parameters = {
            "screen_name":screen_name,
            "include_rts":"false",
            "exclude_replies":"true",
            "count":"10",
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
