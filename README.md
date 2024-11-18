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
    * Phi-V - Microsoft 
    * Paligemma - Google

* Other Notable Free API service providers
  * Google AI studio 
  * Selected models on Huggingface


## Libraries to use for improving efficiency :


### Prompt Engineering Tutorial and tips : 
* Best practices to follow as per [OpenAI](https://platform.openai.com/docs/guides/prompt-engineering) and [Google](https://cloud.google.com/discover/what-is-prompt-engineering#related-google-cloud-products-and-services) 