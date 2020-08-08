import pandas as pd
import torch
from torch.utils.data import Dataset

import config

class TextDataset(Dataset):
    """
    Tweet Dataset for preprocessing text
    """
    def __init__(self, data, target, tokenizer, max_len):
        self.data = data
        self.target = target
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        text = self.data[item]

        encoding = self.tokenizer.encode_plus(
                text,
                truncation=True,
                max_length=self.max_len,
                add_special_tokens=True, # Add '[CLS]' and '[SEP]'
                return_token_type_ids=False,
                pad_to_max_length=True,
                return_attention_mask=True,
                return_tensors='pt',  # Return PyTorch tensors
        )

        return {
            "text":text,
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "targets": torch.tensor(self.target[item], dtype=torch.long)
        }

def main():
    data = pd.read_csv("./data/twitter_sentiment.csv")
    data["sentiment"].replace({"positive": 2, "neutral": 1, "negative": 0}, inplace=True)
    dataset = TweetDataset(data["text"], data["sentiment"], config.TOKENIZER, config.MAX_LEN)
    print(dataset[7])

if __name__ == "__main__":
    main()



