from openai import OpenAI

def gen_story(items:dict):
    style = input("Enter the style of story to generate\n")

    client = OpenAI(
        base_url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct/v1",
        api_key="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"
    )

    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": f"You are a short story teller. Create a {style} short story, less than 200 characters long, using ONLY the given items. Ensure that the correct amount of items are always present in the story. Do not create objects or people that are not provided to you. The format for the items given is (amount:object)." },
            {"role": "user", "content": f"Create a story using these objects:{items}. DO NOT add anything to the story that is not in this list!"}
        ],
        stream=False
    )

    return chat_completion.choices[0].message.content