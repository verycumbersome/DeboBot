"""Config file"""
import os
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# Data Scraping
CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
OAUTH_TOKEN = os.environ.get("TWITTER_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_TOKEN_SECRET")

# TWITTER_NAMES = [
    # "EvergreenGothic",
    # "OlympiaGothic",
    # "OlympiaNice",
    # "LaceyGothic",
    # "HarborGothic",
    # "overheardwwu",
    # "WWUgothic"
# ]
STOP_WORDS = [
    "nigger",
    "nigga",
    "fag",
    "faggot",
    "dyke",
    ]
TWITTER_NAMES = [
    # "vsshole",
    # "camposting",
    # "darth_erogenous",
    # "killmefam",
    # "dril",
    # "poop420guy69",
    "PeterXinping",
    # "toomuchprotein",
    # "rockanrollphoto"
    # "inclcore",
]
SCRAPE_TIMELINE_COUNT = 5000
SCRAPE_DEPTH = 900
