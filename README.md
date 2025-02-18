# Video Analysis and Description Tutorial Project

This project is designed as a learning resource for students to understand how to build AI-powered video analysis applications. It demonstrates the integration of computer vision, large language models, and web technologies.

## Project Overview

This tutorial project shows how to:
1. Process video streams in real-time
2. Generate descriptions of video frames using AI models (Groq, Gemini)
3. Build a web interface for video analysis
4. Handle asynchronous processing and real-time updates

## Prerequisites

- Python 3.8+
- OpenCV
- Flask
- Groq API access
- Google AI Studio access (optional, for Gemini features)

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd Vidreason_tutorial
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Set up API keys:
   - Get a Groq API key from [Groq Console](https://console.groq.com)
   - (Optional) Get a Google AI Studio API key from [Google AI Studio](https://makersuite.google.com/)

5. Configure API keys:
   - For Groq: Update the API key in `web_video_describe.py`
   - For Gemini: Set GOOGLE_API_KEY environment variable or update in `aistudio.py`

## Project Structure

- `web_video_describe.py`: Main application for video processing and web interface
- `aistudio.py`: Google AI Studio integration for image analysis
- `templates/index.html`: Web interface template
- Other utility files for image processing and API interactions

## How to Run

1. Start the web application:
```bash
python web_video_describe.py
```

2. Open browser at `http://localhost:5000`
3. Enter the path to a video file
4. Watch as the AI generates descriptions in real-time!

## Experimentation Tips

### 1. Trying Different Models
- The project uses Groq's LLaMA model by default
- You can experiment with different models by modifying the model parameter in `process_frame()`
- Try adjusting temperature and other parameters to see how they affect descriptions

### 2. Customizing Video Processing
- Modify frame processing rate in `generate_frames()`
- Experiment with different frame extraction methods
- Add pre-processing steps to improve AI analysis

### 3. Enhancing the Interface
- Customize the web interface in `templates/index.html`
- Add new features like saving descriptions
- Implement video upload functionality

## Advanced Topics

### 1. Performance Optimization
- Implement frame buffering
- Add caching for processed frames
- Optimize frame extraction rate

### 2. Error Handling
- Implement retry mechanisms for API calls
- Add proper logging
- Handle various edge cases

### 3. Extended Features
- Add support for multiple video formats
- Implement video segment analysis
- Add export functionality for generated descriptions

## Learning Resources

Basic Yolo and OpenCV tutorial [colab](https://colab.research.google.com/drive/1P1wiN11EHkDPspFLbMPly76tV99InHnI)

# Vidreason_tutorial
Tutorial and sample scripts to run and experiment with multimodal LLMs for surveillance and image analysis based tasks

[colab demo](https://colab.research.google.com/drive/1neuY4X591AHBCd6JwaHo6DBXQvFuOagX?authuser=0#scrollTo=5e10u_gR6v_6) 


## List of Opensource vision LLMs :
* [Groq API](https://console.groq.com/docs/vision)
  
* For On Device Testing
  * 2B parameters : consumes approx 2-6 GB Ram/VRam depending on the quantisation
    * [Moondream2](https://huggingface.co/vikhyatk/moondream2) - Strong and Performant 
  
  * 3B parameters : consumes approx 3-8 GB Ram/VRam depending on the quantisation
    * [MiniCPM-V](https://huggingface.co/openbmb/MiniCPM-V) - Small model but highly efficient for Visual Question Answering    
    * [Phi-3.5](https://huggingface.co/microsoft/Phi-3.5-vision-instruct) - Microsoft 
    * [Paligemma](https://huggingface.co/blog/paligemma) - Google

* Other Notable Free API service providers
  * Google AI studio 
  * Selected models on Huggingface

## Libraries to use for improving efficiency :
* [Bits and Bytes](https://github.com/bitsandbytes-foundation/bitsandbytes) : Compatible with huggingFace and transformers, helps run quantised models in GPU contrained environment
* [VLM Inference](https://docs.vllm.ai/en/latest/models/vlm.html) : Optimises inference speed for supported Vision and Language models. 
### Prompt Engineering Tutorial and tips : 
* Best practices to follow as per [OpenAI](https://platform.openai.com/docs/guides/prompt-engineering) and [Google](https://cloud.google.com/discover/what-is-prompt-engineering#related-google-cloud-products-and-services) 

### Computer Vision
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyImageSearch Tutorials](https://pyimagesearch.com/)

### AI/ML
- [Groq Documentation](https://console.groq.com/docs)
- [Google AI Documentation](https://ai.google.dev/)

### Web Development
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## Contributing

Feel free to:
- Experiment with the code
- Add new features
- Submit improvements
- Share your learning experiences

## License

This project is licensed under the MIT License - see the LICENSE file for details.
