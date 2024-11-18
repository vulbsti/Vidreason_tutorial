from groq import Groq
import base64
API = "Enter API KEY"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your image
image_path = "/home/utka/Pictures/1067737.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

client = Groq(api_key=API)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        },
        {
            "role": "assistant",
            "content": ""
        }
    ],
    model="llama-3.2-11b-vision-preview",
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(chat_completion.choices[0].message.content)
