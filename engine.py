import utils

def main():
    """Main function loop"""
    # ntp_time = utils.get_ntp_time()
    # nonce = utils.get_nonce(32)

    # token = utils.get_token()

    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    parameters = {
        "screen_name":"killmefam",
        "count":"2",
        }
    timeline = utils.make_call(method, url, parameters)
    print(timeline.content)

if __name__ == "__main__":
    main()
