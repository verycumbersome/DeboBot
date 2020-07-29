import ntplib

from time import ctime
from datetime import datetime
from hashlib import sha1
import hmac

def get_ntp_time():
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    ntp_time = round(
            (datetime.now() - datetime.strptime(
                ctime(response.offset),
                "%a %b %d %H:%M:%S %Y")
                ).total_seconds()
            )

    return ntp_time

def get_signature():
    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = b"CONSUMER_SECRET&TOKEN_SECRET"


    # The Base String as specified here:
    raw = b"BASE_STRING" # as specified by OAuth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return hashed.digest().encode("base64").rstrip('\n')
