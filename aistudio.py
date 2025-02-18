"""
Google AI Studio Integration Module

This module demonstrates integration with Google's Generative AI (Gemini) for image analysis.
It provides functions for loading images from different sources and analyzing them using
the Gemini Pro Vision API.

Key Features:
1. Image loading from URLs and local files
2. Error handling and validation
3. Integration with Google's Gemini Pro Vision API
4. Flexible image analysis capabilities

Usage:
    from aistudio import ask_gemini_about_image, load_image_from_filepath
    
    image = load_image_from_filepath("path/to/image.jpg")
    description = ask_gemini_about_image(image, "What's in this image?")
"""

import google.generativeai as genai
import pathlib
import PIL.Image
import requests
import os

# Configure the API key
# For development, you can set the API key directly
# For production, use environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def load_image_from_url(image_url: str) -> PIL.Image.Image:
    """
    Load an image from a given URL.
    
    Args:
        image_url (str): The URL of the image to load
        
    Returns:
        PIL.Image.Image: The loaded image object, or None if loading fails
        
    Example:
        >>> image = load_image_from_url("https://example.com/image.jpg")
        >>> if image:
        ...     print("Image loaded successfully")
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return PIL.Image.open(response.raw)
    except requests.exceptions.RequestException as e:
        print(f"Error loading image from URL: {e}")
        return None

def load_image_from_filepath(file_path: str) -> PIL.Image.Image:
    """
    Load an image from a local file path.
    
    Args:
        file_path (str): Path to the local image file
        
    Returns:
        PIL.Image.Image: The loaded image object, or None if loading fails
        
    Example:
        >>> image = load_image_from_filepath("local/path/to/image.jpg")
        >>> if image:
        ...     print(f"Image loaded with size {image.size}")
    """
    try:
        return PIL.Image.open(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except PIL.UnidentifiedImageError:
        print(f"Error: Could not open or read image file at {file_path}")
        return None

def ask_gemini_about_image(image: PIL.Image.Image, question: str) -> str:
    """
    Use Gemini Pro Vision API to analyze an image and answer questions about it.
    
    Args:
        image (PIL.Image.Image): The image to analyze
        question (str): The question to ask about the image
        
    Returns:
        str: The AI-generated response, or None if an error occurs
        
    Example:
        >>> image = load_image_from_filepath("scene.jpg")
        >>> if image:
        ...     description = ask_gemini_about_image(image, "What objects do you see?")
        ...     print(description)
        
    Note:
        You can experiment with this function by:
        1. Trying different types of questions
        2. Analyzing different image types
        3. Processing multiple images in sequence
    """
    model = genai.GenerativeModel('gemini-exp-1114')

    try:
        response = model.generate_content([question, image])
        return response.text
    except Exception as e:
        print(f"Error querying Gemini Pro Vision API: {e}")
        return None

def main():
    """
    Example usage of the module's functionality.
    
    This function demonstrates:
    1. Loading images from both URLs and local files
    2. Asking questions about the images
    3. Handling responses and errors
    
    Experiment by:
    1. Changing the image sources
    2. Modifying the questions
    3. Adding error handling
    """
    # Example with URL image
    image_url = "https://www.thepinknews.com/wp-content/uploads/2021/12/matrix-red-pill.png?w=792&h=416&crop=1"
    img_from_url = load_image_from_url(image_url)
    if img_from_url:
        question = "What is in this image?"
        answer = ask_gemini_about_image(img_from_url, question)
        if answer:
            print("Answer (from URL):", answer)

    # Example with local file
    file_path = "path/to/your/local/image.jpg"
    img_from_file = load_image_from_filepath(file_path)
    if img_from_file:
        question = "Describe the objects in the image."
        answer = ask_gemini_about_image(img_from_file, question)
        if answer:
            print("Answer (from file path):", answer)

if __name__ == "__main__":
    main()