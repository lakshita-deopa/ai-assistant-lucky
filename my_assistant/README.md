# Lucky — Personal AI Assistant

A full-stack personal AI assistant with natural language chat, AI image generation, and voice interaction — built entirely from scratch using Python and Flask, running locally with GPU acceleration.

## Features

- **Conversational AI Chat** — Natural language conversations powered by Llama 3.2 running locally via Ollama (fully offline, no API costs)
- **AI Image Generation** — Text-to-image generation using Stable Diffusion, accelerated with CUDA on NVIDIA GPU
- **Voice Interaction** — Speech-to-text powered by OpenAI's Whisper, and text-to-speech replies, enabling fully hands-free conversation
- **Conversation Memory** — Maintains context across a chat session
- **Custom Web UI** — Built from scratch with Flask, HTML, CSS, and JavaScript (no third-party UI frameworks)

## Tech Stack

| Backend | Python, Flask |
| LLM | Llama 3.2 via Ollama |
| Image Generation | Stable Diffusion, PyTorch, CUDA, Hugging Face Diffusers |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | pyttsx3 |
| Frontend | HTML, CSS, JavaScript (Vanilla) |

## Architecture

**Request flow:**

1. Browser sends text input or recorded audio to the Flask backend
2. Flask routes the request based on type:
   - Plain text → **Chat module** (Llama 3.2 via Ollama)
   - Image request → **Image generation module** (Stable Diffusion + CUDA)
   - Audio input → **Voice module** (Whisper for transcription, pyttsx3 for speech output)
3. The response (text, image, or audio) is sent back to the browser

## Setup & Installation

### Prerequisites
- Python 3.12
- NVIDIA GPU with CUDA support (recommended for image generation)
- [Ollama](https://ollama.com) installed locally

### Steps

1. Clone this repository:
```bash
git clone https://github.com/lakshita-deopa/ai-assistant-lucky.git
cd ai-assistant-lucky
```

2. Pull the Llama model:
```bash
ollama pull llama3.2
```

3. Create and activate a virtual environment:
```bash
py -3.12 -m venv venv
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the app:
```bash
py app.py
```

6. Open `http://127.0.0.1:5000` in your browser

## How It Works

- **Chat**: User messages are sent to a locally-running Llama 3.2 model via Ollama's REST API, with conversation history maintained for context.
- **Image Generation**: When the assistant detects an image request (via keyword matching), it extracts the prompt and runs it through a locally-loaded Stable Diffusion pipeline accelerated by CUDA.
- **Voice**: Audio recorded in-browser via the MediaRecorder API is sent to the backend, transcribed using Whisper, processed as a normal chat message, and the reply is converted back to speech and played back automatically.

## Future Improvements

- Persistent conversation memory using a database
- Wake-word activation
- Deployment as a desktop application

## Author

**Lakshita Deopa** — 2nd Year B.Tech CSE Student

---
*Built as a personal project to explore practical applications of LLMs, computer vision, and speech AI.*