from flask import Flask, render_template, request, send_file
from groq import Groq
import base64
import os

app = Flask(__name__)
groqAPI = os.getenv('Groq_API_KEY')  # Set your API key as environment variable

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_path = None
    
    if request.method == 'POST':
        image_path = request.form['image_path']
        prompt = request.form['prompt']
        
        if os.path.exists(image_path):
            try:
                base64_image = encode_image(image_path)
                client = Groq(api_key=groqAPI)
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                
                result = chat_completion.choices[0].message.content
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            result = "Error: Image file not found"
    
    return render_template('index_image.html', result=result, image_path=image_path)

@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(port=5050, debug=True)