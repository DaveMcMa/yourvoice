import gradio as gr
import requests
import base64
import tempfile
import os

# Configuration from environment variables
API_URL = os.getenv("TTS_API_URL", "https://rundmc-chatterbox-predictor-david-mcmahon3--d663820b.ingress.dd.demo.local/")
TOKEN = os.getenv("TTS_API_TOKEN", "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTI4NDkyMzEsImlzcyI6ImFpb2xpQGhwZS5jb20iLCJzdWIiOiIwZGU0ODVlNi1hZDg2LTRkZmYtODRhYi0xYTEyOTc3ZDc1OTMiLCJ1c2VyIjoiZGF2aWQubWNtYWhvbjMtaHBlLmNvbSJ9.dZYs589-fTs1YmWFruyKUdYnqUt5teoDF7cc_waq6hVzsddjRuDedUbFIU4L72BLQYMSLlCbbVaJaxiwtZob0FJBOJb6eGJCWW5SPa4YgWjJ51ve2-zmq09DNXPP2HH1Gc3UTFrBn42T28Z1dYpo9-AJ-579cNYAfIDWclButyy03Kamkx-YQ5u4FYnoRSsWd1hibVbtwN5PKIRZc25RtBjFEvDe0i4ILjjgVf2nCvf8qz6GsY-gqWsDwn_X9jUuFEVuJx7mkAFbkTge6DB6g0YCTpuRjileZm4zO4qYIcRSK8TMEdl6ZIjhp48pzVmyuHYm4x4FSAdiG3k_LUjWBA")

def encode_audio_to_base64(audio_file):
    """Convert audio file to base64 string"""
    if audio_file is None:
        return None
    
    with open(audio_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def test_api_connection(api_url, api_token):
    """Test the API connection with provided credentials"""
    if not api_url or not api_token:
        return "Please provide both API URL and token."
    
    try:
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # Simple test payload
        data = {
            "text": "Test connection",
            "exaggeration": 0.4,
            "cfg_weight": 0.4
        }
        
        response = requests.post(
            api_url + "synthesize", 
            headers=headers, 
            json=data, 
            verify=False,
            timeout=10
        )
        
        if response.status_code == 200:
            return "✅ API connection successful!"
        else:
            return f"❌ API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"❌ Connection failed: {str(e)}"

def update_api_settings(api_url, api_token):
    """Update global API settings"""
    global API_URL, TOKEN
    if api_url:
        API_URL = api_url
    if api_token:
        TOKEN = api_token
    return "Settings updated successfully!"

def synthesize_speech(audio_input, text_input, exaggeration, cfg_weight):
    """Call the TTS API with the provided audio and text"""
    if not text_input:
        return None, "Please provide text input."
    
    try:
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text_input,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight
        }
        
        # Add audio prompt only if provided
        if audio_input:
            audio_b64 = encode_audio_to_base64(audio_input)
            if audio_b64:
                data["audio_prompt_base64"] = audio_b64
        
        # Make API call
        response = requests.post(
            API_URL + "synthesize", 
            headers=headers, 
            json=data, 
            verify=False
        )
        
        if response.status_code == 200:
            # Save the response audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(response.content)
                return tmp_file.name, "Speech synthesized successfully!"
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return None, f"Error: {str(e)}"

def create_app():
    """Create the Gradio interface"""
    
    # Load logo
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode("utf-8")
        
        header_html = f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_data}" alt="HPE Logo" 
                 style="max-height: 40px; max-width: 40px; width: auto; height: auto; object-fit: contain;" />
            <h1 style="margin: 0; color: #2c3e50;">Your Voice - Text to Speech powered by HPE Private Cloud AI</h1>
        </div>
        """
    else:
        header_html = """
        <div style="margin-bottom: 20px;">
            <h1 style="margin: 0; color: #2c3e50;">Your Voice - Text to Speech powered by HPE Private Cloud AI</h1>
        </div>
        """
    
    # Try with predefined color closest to HPE Green
    hpe_theme = gr.themes.Soft(
        primary_hue="emerald",
    )
    
    with gr.Blocks(title="Your Voice - TTS", theme=hpe_theme) as app:
        gr.Markdown(header_html)
        
        with gr.Tabs():
            with gr.Tab("About"):
                gr.Markdown("""
                ## About Your Voice - text to Speech Synthesis
                
                This application provides advanced text-to-speech synthesis powered by HPE Private Cloud AI. 
                
                **Features:**
                - **Voice Cloning**: Upload your own audio sample to clone a specific voice
                - **Default Voice**: Use without audio sample for the default model voice
                - **Customizable Parameters**: Adjust exaggeration and CFG weight for fine-tuned results
                - **High Quality**: Powered by the ResembleAI Chatterbox model
                
                **How to use:**
                1. Optionally provide a voice sample to clone
                2. Enter the text you want to synthesize
                3. Adjust parameters as needed
                4. Generate speech and download the result
                
                ---
                """)
                
                gr.Markdown("### API Configuration")
                with gr.Row():
                    with gr.Column():
                        api_url_input = gr.Textbox(
                            label="API Endpoint URL",
                            value=API_URL,
                            placeholder="https://your-api-endpoint.com/"
                        )
                        api_token_input = gr.Textbox(
                            label="API Token",
                            value=TOKEN,
                            type="password",
                            placeholder="Enter your API token"
                        )
                        
                        with gr.Row():
                            test_btn = gr.Button("Test Connection", variant="secondary")
                            update_btn = gr.Button("Update Settings", variant="primary")
                        
                        connection_status = gr.Textbox(
                            label="Connection Status",
                            interactive=False
                        )
                
                # Connect test and update functions
                test_btn.click(
                    fn=test_api_connection,
                    inputs=[api_url_input, api_token_input],
                    outputs=connection_status
                )
                
                update_btn.click(
                    fn=update_api_settings,
                    inputs=[api_url_input, api_token_input],
                    outputs=connection_status
                )
            
            with gr.Tab("Synthesize Speech"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Provide voice sample to be cloned (optional)")
                        audio_input = gr.Audio(
                            show_label=False,
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        
                        gr.Markdown("### Enter text to synthesize")
                        text_input = gr.Textbox(
                            show_label=False,
                            placeholder="Enter the text you want to convert to speech...",
                            lines=3
                        )
                        
                        with gr.Row():
                            exaggeration = gr.Slider(
                                minimum=0.0,
                                maximum=1.0,
                                value=0.4,
                                step=0.1,
                                label="Exaggeration",
                                info="How much to exaggerate the voice characteristics"
                            )
                            
                            cfg_weight = gr.Slider(
                                minimum=0.0,
                                maximum=1.0,
                                value=0.4,
                                step=0.1,
                                label="CFG Weight",
                                info="Classifier-free guidance weight"
                            )
                        
                        synthesize_btn = gr.Button("Generate Speech", variant="primary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### Generated Speech")
                        output_audio = gr.Audio(type="filepath", show_label=False)
                        status_msg = gr.Textbox(interactive=False, show_label=False)
                
                # Connect the synthesis interface
                synthesize_btn.click(
                    fn=synthesize_speech,
                    inputs=[audio_input, text_input, exaggeration, cfg_weight],
                    outputs=[output_audio, status_msg]
                )
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)