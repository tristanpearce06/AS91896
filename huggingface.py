# from huggingface_hub import login
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from transformers import pipeline

# login(token = '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')

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B", cache_dir="/kaggle/working/")

# model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B", cache_dir="/kaggle/working/", device_map="auto",)

from openai import OpenAI

# init the client but point it to TGI
client = OpenAI(
    # replace with your endpoint url, make sure to include "v1/" at the end
    base_url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct/v1",
    # replace with your API key
    api_key="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"
)

chat_completion = client.chat.completions.create(
    model="tgi",
    messages=[
        {"role": "system", "content": "You are Ryan Gosling in Lala Land." },
        {"role": "user", "content": "Did you end up with her?"}
    ],
    stream=True
)

# iterate and print stream
for message in chat_completion:
    print(message.choices[0].delta.content, end="")