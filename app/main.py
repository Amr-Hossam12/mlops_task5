import gradio as gr
import requests
from fastapi import FastAPI

# Ollama local API endpoint
LOCAL_OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# Main text generation function
def generate_text(prompt: str, model_name: str):
    if not prompt.strip():
        return "Please enter a message before generating a response."
    
    try:
        # Prepare request for Ollama local model
        data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(LOCAL_OLLAMA_ENDPOINT, json=data)
        response.raise_for_status()

        # Extract model response
        result = response.json().get("response", "The model did not return any output.")
        return result

    except requests.exceptions.ConnectionError:
        return "Unable to connect to Ollama. Make sure the Ollama server is running locally."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Example local models (you can replace with yours)
model_dropdown = gr.Dropdown(
    choices=["deepseek-r1:1.5b"],
    value="deepseek-r1:1.5b",
    label="Choose Your Local Model"
)

# Gradio interface
gui = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(
            lines=4,
            label="Enter Your Prompt",
            placeholder="Ask your AI assistant..."
        ),
        model_dropdown
    ],
    outputs=gr.Textbox(
        label="Model Output",
        lines=15,
        max_lines=25,
        show_copy_button=True
    ),
    title="Local AI Coding Assistant",
    description="A fully local AI chat assistant."
)

# FastAPI integration
app = FastAPI(title="Local AI Assistant API")
app = gr.mount_gradio_app(app, gui, path="/")
