import torch
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel


if torch.cuda.is_available():
    device=torch.device("cuda")
else:
    device = torch.device("cpu")

TOKENIZER = GPT2Tokenizer.from_pretrained(
        "gpt2",
        add_prefix_space=True
        )

MODEL = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=TOKENIZER.eos_token_id)

text = "Hello world"

input_ids = TOKENIZER.encode(text, return_tensors='tf')
greedy_output = MODEL.generate(input_ids, max_length=50)

print("Output:\n" + 100 * '-')
print(TOKENIZER.decode(greedy_output[0], skip_special_tokens=True))

# inputs = TOKENIZER.encode_plus(
        # text,
        # return_tensors="pt"
        # )


# outputs = MODEL(**inputs)
# last_hidden_states = outputs[0]

# output = torch.max(last_hidden_states, dim = 1)

# print(output)
