import requests # Send request to huggingface servers (while praying)
from PIL import Image
from io import BytesIO

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def generate_image_from_text(prompt):
    modifiedPrompt = f"{prompt}, ((art, fantasy, unrealistic, stencil)"
    payload = {
        "inputs": modifiedPrompt,
        "negative_prompt": "out of frame, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    image_bytes = BytesIO(response.content)
    image = Image.open(image_bytes)
    return image