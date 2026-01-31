from openai import OpenAI
import base64

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

# Generate an image using the image model
img = client.images.generate(
    model="dall-e-3",  # or "dall-e-2"
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024",
    response_format="b64_json"  # IMPORTANT
)

# Decode and save the image
image_bytes = base64.b64decode(img.data[0].b64_json)

with open("output.png", "wb") as f:
    f.write(image_bytes)
