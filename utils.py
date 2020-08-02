import os
import ntplib
import urllib.parse
import random

from time import ctime
from datetime import datetime
from hashlib import sha1
import hmac

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")

def get_ntp_time():
    """Return the NTP time diff in seconds"""
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    ntp_time = round(
            (datetime.now() - datetime.strptime(
                ctime(response.offset),
                "%a %b %d %H:%M:%S %Y")
                ).total_seconds()
            )

    return ntp_time

def get_nonce(length=8):
    """Generate pseudorandom number"""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def get_token():
    oauth_callback = "https%3A%2F%2Ftwitter.com"
    oauth_signature_method = "HMAC-SHA1"
    oauth_timestamp = get_ntp_time()
    oauth_consumer_key = consumer_key
    # oauth_signature = get_signature
    oauth_version = "1.0"

    get_signature(oauth_consumer_key, "")


def get_signature(consumer_secret, token_secret):
    """Create API request signature"""
    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = (consumer_secret + "&" + token_secret).encode()
    print(key)

    # key = b"CONSUMER_SECRET&TOKEN_SECRET"


    # The Base String as specified here:
    raw = b"BASE_STRING" # as specified by OAuth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return hashed.digest().encode("base64").rstrip('\n')
