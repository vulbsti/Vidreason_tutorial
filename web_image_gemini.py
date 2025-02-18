from flask import Flask, render_template, request, send_file
import google.generativeai as genai
import PIL.Image
import os


flash = "gemini-2.0-flash"
flash_lite = "gemini-2.0-flash-lite-preview-02-05"
flash_think = "gemini-2.0-flash-thinking-exp-01-21"

app = Flask(__name__)

# Configure Google AI API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Set your API key as environment variable
genai.configure(api_key=GOOGLE_API_KEY)

def load_and_analyze_image(image_path, prompt):
    try:
        # Load the image
        image = PIL.Image.open(image_path)
        
        # Initialize Gemini model
        model = genai.GenerativeModel(flash_lite)

        # Generate response
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_path = None
    
    if request.method == 'POST':
        image_path = request.form['image_path']
        prompt = request.form['prompt']
        
        if os.path.exists(image_path):
            result = load_and_analyze_image(image_path, prompt)
        else:
            result = "Error: Image file not found"
    
    return render_template('index_image.html', result=result, image_path=image_path)

@app.route('/image/<path:filename>')
def serve_image(filename):
    try:
        if os.path.isabs(filename):
            # If it's an absolute path, use it directly
            if os.path.exists(filename):
                return send_file(filename)
        return "Image not found", 404
    except Exception as e:
        return f"Error loading image: {str(e)}", 400

if __name__ == '__main__':
    app.run(port=5051, debug=True)