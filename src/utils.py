"""Utils for Twitter API"""
import os
import base64
import random
import hmac
from datetime import datetime
from hashlib import sha1
from time import ctime
import tqdm
import requests
import urllib
import ntplib
import pandas as pd

import config

file_dir = os.path.dirname(__file__)


def get_random_tweet():
    """Returns a random tweet from the directory of generated tweets"""
    tweets = []
    text_path = os.path.join(file_dir, "../text/")
    for file in os.listdir(text_path):
        with open(text_path + file, "r") as fp:
            tweets.extend(fp.read().split("<|startoftext|>"))

    # Remove duplicates and exd of text
    tweets = list(set([tweet.replace("<|endoftext|>", "") for tweet in tweets]))

    # Checks if the generated tweets is in the orignal dataset
    training = []
    csv_dir_path = os.path.join(file_dir, "data/")
    for csv_path in os.listdir(csv_dir_path):
        if csv_path.endswith(".csv"):
            training.append(pd.read_csv(os.path.join(csv_dir_path, csv_path)))

    # Combine all csv into one dataframe
    training = pd.concat(training, ignore_index=True)

    while(True):
        # Select a random tweet from the options
        tweet = random.choice(tweets)

        # Check for both originality of a tweet and if the tweet contains any offensive stop words
        unoriginal = [True for item in training["text"] if str(tweet).lower() == str(item).lower()]
        offensive = [True for item in config.STOP_WORDS if item in tweet]

        if not (unoriginal or offensive):
            return tweet.strip()


def csv_to_txt(path):
    """Converts a CSV file to a TXT file to the /data/ directory"""
    output = []

    # Add all values from csv files in data/ to output
    csv_dir_path = os.path.join(file_dir, "data/")
    for csv_path in os.listdir(csv_dir_path):
        if csv_path.endswith(".csv"):
            data = pd.read_csv(os.path.join(csv_dir_path, csv_path)).dropna()

            print("Writing file to txt")
            for item in tqdm.tqdm(data["text"]):
                item = "<|startoftext|>" + item + "<|endoftext|>\n"
                output.append(item)

    textfile_path = os.path.join(file_dir, "../textdata.txt")
    with open(textfile_path, "w+") as file:
        for item in output:
            file.write(item)



def percent_encoding(string):
    """Percent encode a string"""
    result = ''
    accept = [char for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~'
        .encode('utf-8')]

    for char in string.encode('utf-8'):
        result += chr(char) if char in accept else '%{}'.format(hex(char)[2:]).upper()
    return result


def get_ntp_time():
    """Return the NTP time diff in seconds"""
    while True:
        try:
            client = ntplib.NTPClient()
            response = client.request('europe.pool.ntp.org', version=3)
            ntp_time = round(
                (datetime.now() - datetime.strptime(
                    ctime(response.offset),
                    "%a %b %d %H:%M:%S %Y")
                ).total_seconds()
            )

            return ntp_time

        except Exception:
            pass


def get_nonce(length=32):
    """Generate psuedorandom Nonce"""
    randnum = random.randint(10 ** (length - 1), (10 ** length) - 1)
    data = base64.b64encode(str(randnum).encode())

    return data[:length] + (data[length:] and b"")


def make_call(method, url, parameters):
    """Make a call to the Twitter API"""
    auth = {
        "oauth_consumer_key": config.CONSUMER_KEY,
        "oauth_nonce": get_nonce(32).decode(),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": get_ntp_time(),
        "oauth_token": config.OAUTH_TOKEN,
        "oauth_version": "1.0",
        }

    auth["oauth_signature"] = get_signature(
        method,
        url,
        config.OAUTH_TOKEN_SECRET,
        {**parameters, **auth}
        ).decode("utf-8")

    # Format Oauth authorization header
    dst = "OAuth"
    for item in auth.items():
        dst += " " + percent_encoding(item[0]) + "=\"" + percent_encoding(str(item[1])) + "\","
    dst = dst[:-1]

    if method == "GET":
        return requests.get(
            url,
            params=parameters,
            headers={'Authorization': dst}
            )

    if method == "POST":
        return requests.post(
            url,
            data=parameters,
            headers={'Authorization': dst}
            )


def get_signature(method, url, token_secret, parameters):
    """Create API request signature"""
    # Generate parameter string
    parameter_string = ""
    sorted_params = {k: str(parameters[k]) for k in sorted(parameters)}

    for item in sorted_params.items():
        parameter_string += "&" + percent_encoding(item[0]) + "=" + percent_encoding(str(item[1]))

    # Append percent encoded method url and parameter string
    output = method + "&" + percent_encoding(url) + "&" + percent_encoding(parameter_string[1:])

    key = (percent_encoding(config.CONSUMER_SECRET) + "&" + percent_encoding(token_secret)).encode()

    # Generate hash
    hashed = hmac.new(key, output.encode(), sha1)

    return base64.b64encode(hashed.digest()).strip()
