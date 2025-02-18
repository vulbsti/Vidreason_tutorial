import google.generativeai as genai
import pathlib
import PIL.Image
import requests
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np
from dotenv import load_dotenv
from vertexai.vision_models import Image, MultiModalEmbeddingModel

load_dotenv()

# Configure the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")
genai.configure(api_key=GOOGLE_API_KEY)


# Models Provided by Google as of 2025-02-15
flash_lite = "gemini-2.0-flash-lite-preview-02-05"
flash_2 = "gemini-2.0-flash"
flash_think = "gemini-2.0-flash-thinking-exp-01-21"

# Initialize models
gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')

# TODO(developer): Try different dimenions: 128, 256, 512, 1408
embedding_dimension = 128
embedding_model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")


# Initialize Qdrant client (local instance) for storing image details in a vector database
qdrant_client = QdrantClient(":memory:")
#Initialise Qdrant client with the database path, if you want to use a persistent database (Example:
#qdrant_client = QdrantClient("qdra.db")    
COLLECTION_NAME = "image_collection"


def setup_vector_db():
    """Setup the vector database collection"""
    try:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=embedding_dimension, distance=Distance.COSINE),
        )
        print("Vector database collection created successfully")
    except Exception as e:
        print(f"Collection might already exist: {e}")

def store_image_in_vectordb(image_path, image_description=None):
    """
    Process and store image in vector database
    Args:
        image_path: Path to the image file
        image_description: Optional manual description of the image
    Returns:
        bool: Success status
    """
    try:
        # Load and process image
        image = PIL.Image.open(image_path)
        
        # Generate image description if not provided
        if not image_description:
            response = gemini_model.generate_content(["Describe this image in detail", image])
            image_description = response.text

        # Generate vector embedding for the description
        embedding_response = embedding_model.embed_content(
            image_description,
            task_type="retrieval_document"
        )
        embedding = embedding_response.embedding

        # Store in Qdrant
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=hash(image_path),  # Using hash of path as ID
                    vector=embedding,
                    payload={
                        "image_path": str(image_path),
                        "description": image_description
                    }
                )
            ]
        )
        print(f"Successfully stored image: {image_path}")
        return True
    except Exception as e:
        print(f"Error storing image: {e}")
        return False

def search_images(query, limit=5):
    """
    Search for images based on text query
    Args:
        query: Text query to search for
        limit: Maximum number of results to return
    Returns:
        list: List of matching image paths and descriptions
    """
    try:
        # Generate embedding for the query
        query_embedding = embedding_model.embed_content(
            query,
            task_type="retrieval_query"
        ).embedding

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                'image_path': result.payload['image_path'],
                'description': result.payload['description'],
                'similarity_score': result.score
            })
        
        return results
    except Exception as e:
        print(f"Error searching images: {e}")
        return []

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
    model = genai.GenerativeModel(model_id = flash_lite)

    try:
        response = model.generate_content([question, image])
        return response.text
    except Exception as e:
        print(f"Error querying Gemini Pro Vision API: {e}")
        return None


def main():
    # Setup vector database
    setup_vector_db()
    
    # Example usage
    image_folder = "path/to/your/images"  # Replace with your image folder path
    
    # Store some images
    if os.path.exists(image_folder):
        for image_file in os.listdir(image_folder):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(image_folder, image_file)
                store_image_in_vectordb(image_path)
    
    # Example search
    search_query = "Show me pictures of people standing"
    results = search_images(search_query)
    
    print("\nSearch Results:")
    for result in results:
        print(f"\nImage: {result['image_path']}")
        print(f"Description: {result['description']}")
        print(f"Similarity Score: {result['similarity_score']}")

if __name__ == "__main__":
    main()
