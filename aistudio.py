import google.generativeai as genai
import pathlib
import PIL.Image
import requests
import os

# Configure the API key (replace with your key directly if not using env var)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # For prod usage, use environment variable.
GOOGLE_API_KEY = "Enter API KEY"
genai.configure(api_key=GOOGLE_API_KEY)


def load_image_from_url(image_url):
    """Loads an image from a URL."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return PIL.Image.open(response.raw)
    except requests.exceptions.RequestException as e:
        print(f"Error loading image from URL: {e}")
        return None


def load_image_from_filepath(file_path):
    """Loads an image from a file path."""
    try:
        return PIL.Image.open(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except PIL.UnidentifiedImageError:
        print(f"Error: Could not open or read image file at {file_path}")
        return None


def ask_gemini_about_image(image, question):
    """Asks a question about the image using Gemini Pro Vision API."""
    model = genai.GenerativeModel('gemini-exp-1114')

    try:
        response = model.generate_content([question, image])
        return response.text
    except Exception as e:
        print(f"Error querying Gemini Pro Vision API: {e}")
        return None


def main():
    # Example usage:
    # Replace with your image URL
    file_path = "path/to/your/local/image.jpg"  # Replace with your local image path
    image_url = "https://www.thepinknews.com/wp-content/uploads/2021/12/matrix-red-pill.png?w=792&h=416&crop=1"

    # --- Option 1: Load image from URL ---
    img_from_url = load_image_from_url(image_url)
    if img_from_url:
        question = "What is in this image?"
        answer = ask_gemini_about_image(img_from_url, question)
        if answer:
            print("Answer (from URL):", answer)

    # --- Option 2: Load image from file path ---
    
    img_from_file = load_image_from_filepath(file_path)

    if img_from_file:
        question = "Describe the objects in the image."
        answer = ask_gemini_about_image(img_from_file, question)
        if answer:
            print("Answer (from file path):", answer)


if __name__ == "__main__":
    main()
