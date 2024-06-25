import object_rec

print("Capturing frame")

ret, frame = object_rec.captureFrame()

print("frame captured")
print("creating model")

modelresults = object_rec.model(frame)

print("model created")
print("finding objects")

detected_obj = object_rec.returnFoundObjects(modelresults)

print("objects found")

print(detected_obj)

from openai import OpenAI

print("generating story")

client = OpenAI(
    base_url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct/v1",
    api_key="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"
)

chat_completion = client.chat.completions.create(
    model="tgi",
    messages=[
        {"role": "system", "content": "You are a short story teller. Create a short story, less than 200 characters long, using ONLY the given items. Ensure that the correct amount of items are always present in the story. The format for the items given is (amount:object)" },
        {"role": "user", "content": f"{detected_obj}"}
    ],
    stream=True
)

for message in chat_completion:
    print(message.choices[0].delta.content, end="")