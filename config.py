import os
import logging
import gpt_2_simple as gpt2

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
OAUTH_TOKEN = os.environ.get("TWITTER_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_TOKEN_SECRET")
TWITTER_NAMES = [
    # "darth_erogenous",
    # "adda_boi",
    "killmefam",
    "poop420guy69",
    "toomuchprotein",
    "inclcore",
    "rockanrollphoto"
]
SCRAPE_TIMELINE_COUNT = 5000
SCRAPE_DEPTH = 100

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)
