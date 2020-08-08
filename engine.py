import sys
import json
import re
import pandas as pd
import tqdm
import torch
import re
import numpy as np
import tensorflow as tf
import gpt_2_simple as gpt2
import os
import requests

import config
import utils
from model import GPT2Model


def get_timeline(screen_name, depth):
    """Function to return values from a user's timeline"""
    max_id = 0
    data = []
    method = "GET"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    print("Scraping tweets from \'" + screen_name + "\'")
    for i in tqdm.tqdm(range(depth)):
        parameters = {
            "max_id":max_id - 1,
            "screen_name":screen_name,
            "include_rts":"false",
            "exclude_replies":"true",
            "tweet_mode":"extended",
            "count":str(config.SCRAPE_TIMELINE_COUNT),
            }
        if not max_id: parameters.pop("max_id")

        timeline = utils.make_call(method, url, parameters)

        for item in json.loads(timeline.content):
            max_id = item["id"]
            text = re.sub(r"http\S+", "", item["full_text"]) + "<eos>"
            data.append(text)

    return data

def main():
    """Main function"""
    if "--scrape" in sys.argv:
        data = {"text":[]}

        for screen_name in config.TWITTER_NAMES:
            data["text"].extend(get_timeline(screen_name, config.SCRAPE_DEPTH))

        df = pd.DataFrame(data=data)
        df.to_csv("data/textdata.csv", index=False)

    if "--txt" in sys.argv:
        utils.convert_to_txt("data/textdata.csv")

    if "--gen" in sys.argv:
        # model = GPT2Model(config.MODEL_CONFIG)
        # model.load_state_dict(torch.load(config.MODEL_PATH, map_location=torch.device('cpu')))

        model_name = "124M"
        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

        file_name = "data/textdata.txt"
        sess = gpt2.start_tf_sess()
        gpt2.finetune(sess,
                      file_name,
                      model_name=model_name,
                      steps=1000)   # steps is max number of training steps

        gpt2.generate(sess)



        # model = torch.load(config.MODEL_PATH, map_location=torch.device('cpu'))
        # print(model)

        # review_text = "I love completing my todos! Best app ever!!!"
        # while(True):
        # review_text = input("Enter Tweet:")
        # encoded_review = config.TOKENIZER.encode_plus(
                # text=review_text,
                # truncation=True,
                # max_length=config.MAX_LEN,
                # add_special_tokens=True,
                # return_token_type_ids=False,
                # pad_to_max_length=True,
                # return_attention_mask=True,
                # return_tensors='pt',
                # )

        # print(encoded_review)

        # input_ids = encoded_review['input_ids'].to(device)
        # attention_mask = encoded_review['attention_mask'].to(device)
        # output = model(
                # input_ids=input_ids,
                # attention_mask=attention_mask
                # )
        # _, prediction = torch.max(output, dim=1)
        # print(prediction)
        # print(f'Review text: {review_text}')
        # print(f'Sentiment  : {class_names[prediction]}')


if __name__ == "__main__":
    main()
