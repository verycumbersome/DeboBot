import os
import ntplib
import urllib.parse
import random
import base64
import requests

from requests_oauthlib import OAuth1
from collections import OrderedDict
from time import ctime
from datetime import datetime
from hashlib import sha1
import hmac

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")

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
    """Generate pseudorandom number"""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def get_token():
    """Get OAuth Access token"""

    url = "https://api.twitter.com/oauth/request_token"
    parameters = {
        "oauth_consumer_key":consumer_key,
        "oauth_nonce":get_nonce(),
        "oauth_callback":"https%3A%2F%2Ftwitter.com",
        "oauth_signature_method":"HMAC-SHA1",
        "oauth_timestamp":get_ntp_time(),
        "oauth_version":"1.0",
        }

    parameters["oauth_signature"] = get_signature(
            "POST",
            url,
            parameters["oauth_consumer_key"],
            "",
            parameters
            ).decode("utf-8")

    dst = "Oauth"

    for item in parameters.items():
        dst += " " + percent_encoding(item[0]) + "=\"" + percent_encoding(str(item[1])) + "\","

    dst = dst[:-1]
    print(dst)
    # requests.get(url, auth=auth)


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

    hashed = hmac.new(key, output.encode(), sha1)

    # The signature
    return base64.b64encode(hashed.digest())
