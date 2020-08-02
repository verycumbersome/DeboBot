import os
import ntplib
import urllib.parse
import random
import base64
import requests
import logging

from requests_oauthlib import OAuth1
from collections import OrderedDict
from time import ctime
from datetime import datetime
from hashlib import sha1
import hmac

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
oauth_token = "350639912-pPdscEZxEm0XpaeeekuBvtg6eqMpLXYqlwWbnz18"
oauth_token_secret = "qdQTI4evVHaSriYx759GiHkKylekCleaKyMdawChwAA8h"

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def percent_encoding(string):
    """Percent encode a string"""
    result = ''
    accepted = [c for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~'.encode('utf-8')]
    for char in string.encode('utf-8'):
        result += chr(char) if char in accepted else '%{}'.format(hex(char)[2:]).upper()
    return result

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
    """Generate psuedorandom Nonce"""

    randnum = random.randint(10 ** length, (10 ** (length + 1)) - 1)
    return base64.b64encode(str(randnum).encode())

def get_timeline(user, count):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    auth = {
        "oauth_consumer_key":consumer_key,
        "oauth_nonce":get_nonce(32).decode("utf-8"),
        "oauth_signature_method":"HMAC-SHA1",
        "oauth_timestamp":get_ntp_time(),
        "oauth_token":oauth_token,
        "oauth_version":"1.0",
        }
    parameters = {
        "screen_name":user,
        "count":str(count),
        }

    auth["oauth_signature"] = get_signature(
            "POST",
            url,
            consumer_secret,
            oauth_token_secret,
            {**parameters, **auth}
            ).decode("utf-8")

    auth = {k: percent_encoding(str(auth[k])) for k in sorted(auth)}

    # Format Oauth authorization header
    dst = "OAuth"
    for item in auth.items():
        dst += " " + percent_encoding(item[0]) + "=\"" + percent_encoding(str(item[1])) + "\","
    dst = dst[:-1]

    print("\n\n\n", dst, "\n\n\n")

    timeline = requests.get(
            url,
            params=parameters,
            headers={'Authorization': dst}
            )

    # print(timeline)


def get_signature(method, url, consumer_secret, token_secret, parameters):
    """Create API request signature"""
    output = method + "&" + percent_encoding(url)

    # Sorted parameters for signature
    sorted_params = {k: percent_encoding(str(parameters[k])) for k in sorted(parameters)}

    # Generate signature base string
    for item in sorted_params.items():
        output += "&" + item[0] + "=" + str(item[1])

    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = (consumer_secret + "&" + token_secret).encode()

    hashed = hmac.new(key, percent_encoding(output).encode(), sha1)

    # The signature
    return base64.b64encode(hashed.digest())
