"""Utils for Twitter API"""
import os
import base64
import random
import logging
import hmac
from datetime import datetime
from hashlib import sha1
from time import ctime
import requests
import ntplib

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
oauth_token = os.environ.get("TWITTER_TOKEN")
oauth_token_secret = os.environ.get("TWITTER_TOKEN_SECRET")

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
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

def get_nonce(length=32):
    """Generate psuedorandom Nonce"""

    randnum = random.randint(10 ** (length - 1), (10 ** length) - 1)
    data = base64.b64encode(str(randnum).encode())

    return data[:length] + (data[length:] and b"")

def make_call(method, url, parameters):
    """Make a call to the Twitter API"""
    auth = {
        "oauth_consumer_key":consumer_key,
        "oauth_nonce":get_nonce(32).decode(),
        "oauth_signature_method":"HMAC-SHA1",
        "oauth_timestamp":get_ntp_time(),
        "oauth_token":oauth_token,
        "oauth_version":"1.0",
        }

    auth["oauth_signature"] = get_signature(
        method,
        url,
        oauth_token_secret,
        {**parameters, **auth}
        ).decode("utf-8")

    auth = {k: auth[k] for k in sorted(auth)}

    # Format Oauth authorization header
    dst = "OAuth"
    for item in auth.items():
        dst += " " + percent_encoding(item[0]) + "=\"" + percent_encoding(str(item[1])) + "\","
    dst = dst[:-1]

    return requests.get(
        url,
        params=parameters,
        headers={'Authorization': dst}
        )

def get_signature(method, url, token_secret, parameters):
    """Create API request signature"""
    # output = method + "&" + percent_encoding(url)
    parameter_string = ""

    # Sorted parameters for signature
    sorted_params = {k: percent_encoding(str(parameters[k])) for k in sorted(parameters)}

    # Generate signature base string
    for item in sorted_params.items():
        parameter_string += "&" + percent_encoding(item[0]) + "=" + percent_encoding(str(item[1]))

    output = method + "&" + percent_encoding(url) + "&" + percent_encoding(parameter_string[1:])

    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = (percent_encoding(consumer_secret) + "&" + percent_encoding(token_secret)).encode()

    hashed = hmac.new(key, output.encode(), sha1)

    # The signature
    return base64.b64encode(hashed.digest()).strip()

