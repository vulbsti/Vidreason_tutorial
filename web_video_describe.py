from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from groq import Groq
import base64
import cv2
import numpy as np
import os
from threading import Thread
from queue import Queue
import time
import json

app = Flask(__name__)
description_queues = {}  # Dictionary to store queues for each video path

API = ""
client = Groq(api_key=API)

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def process_frame(frame, prompt):
    base64_frame = encode_frame(frame)
    
    if not prompt:
        prompt = "Describe what is happening in this frame of the video."
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
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

def generate_frames(path, prompt):
    video_id = f"{path}_{prompt}"
    if video_id not in description_queues:
        description_queues[video_id] = Queue()
    
    description_queue = description_queues[video_id]
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    last_processed_second = -1
    
    def process_description(frame, current_second):
        try:
            description = process_frame(frame, prompt)
            description_queue.put((current_second, description))
        except Exception as e:
            print(f"Error processing frame at second {current_second}: {str(e)}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        current_second = frame_count // fps
        
        if current_second > last_processed_second:
            # Process one frame per second
            Thread(target=process_description, args=(frame.copy(), current_second)).start()
            last_processed_second = current_second
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        frame_count += 1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(1/fps)
    
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    video_path = request.args.get('video_path', '')
    prompt = request.args.get('prompt', '')
    if not os.path.exists(video_path):
        return "Video file not found", 404
    
    return Response(generate_frames(video_path, prompt),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/descriptions')
def descriptions():
    video_path = request.args.get('video_path', '')
    prompt = request.args.get('prompt', '')
    if not os.path.exists(video_path):
        return "Video file not found", 404
    
    video_id = f"{video_path}_{prompt}"
    if video_id not in description_queues:
        description_queues[video_id] = Queue()
    
    def generate_descriptions():
        description_queue = description_queues[video_id]
        while True:
            if not description_queue.empty():
                timestamp, description = description_queue.get()
                data = {'timestamp': timestamp, 'description': description}
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(0.1)
    
    return Response(stream_with_context(generate_descriptions()),
                   mimetype='text/event-stream')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_path = request.form.get('video_path')
    prompt = request.form.get('prompt')
    if not os.path.exists(video_path):
        return jsonify({"error": "Video file not found"}), 404
    return jsonify({"status": "success", "video_path": video_path, "prompt": prompt})

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)