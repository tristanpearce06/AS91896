import requests # Send request to huggingface servers (while praying)
from PIL import Image
from io import BytesIO

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def generate_image_from_text(prompt):
    payload = {
        "inputs": prompt,
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    image_bytes = BytesIO(response.content)
    image = Image.open(image_bytes)
    return image
