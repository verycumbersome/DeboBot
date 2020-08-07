import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

TWITTER_NAMES = [
    "killmefam",
    "darth_erogenous",
    "adda_boi",
    "poop420guy69",
    "toomuchprotein",
    "inclcore",
    "rockanrollphoto"
]
COUNT = 5000

