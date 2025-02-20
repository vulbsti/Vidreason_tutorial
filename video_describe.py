from groq import Groq
import base64
import cv2
import numpy as np
import time
from datetime import datetime
import os

API = ""

def encode_frame(frame):
    # Encode frame to base64
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def process_frame(client, frame):
    base64_frame = encode_frame(frame)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image? Describe it briefly."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_frame}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return chat_completion.choices[0].message.content

def process_video(video_path):
    # Initialize Groq client
    client = Groq(api_key=API)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    
    frame_number = 0
    last_processed_second = -1
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        current_second = frame_number // fps
        
        # Process one frame per second
        if current_second > last_processed_second:
            print(f"\nProcessing frame at {current_second} seconds...")
            description = process_frame(client, frame)
            print(f"Description: {description}")
            last_processed_second = current_second
            
        frame_number += 1
        
    cap.release()

if __name__ == "__main__":
    video_path = input("Enter the path to your video file: ")
    process_video(video_path)
