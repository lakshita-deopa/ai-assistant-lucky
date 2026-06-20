from flask import Flask, request, jsonify, render_template, send_file
from assistant import Assistant
from image_generator import ImageGenerator
from voice_handler import VoiceHandler
import os
import tempfile

app = Flask(__name__)
bot = Assistant()
img_gen = ImageGenerator()
voice = VoiceHandler()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message.strip():
        return jsonify({"reply": "", "type": "text"})

    if bot.is_image_request(user_message):
        prompt = bot.extract_image_prompt(user_message)
        img_base64 = img_gen.generate(prompt)
        return jsonify({"reply": img_base64, "type": "image"})

    reply = bot.chat(user_message)
    return jsonify({"reply": reply, "type": "text"})

@app.route("/voice-input", methods=["POST"])
def voice_input():
    audio_file = request.files["audio"]
    temp_path = os.path.join(tempfile.gettempdir(), "user_audio.webm")
    audio_file.save(temp_path)
    print(f"Saved audio to: {temp_path}, size: {os.path.getsize(temp_path)} bytes")
    try:
        text = voice.transcribe(temp_path)
        print(f"Transcription result: '{text}'")
    except Exception as e:
        print(f"Transcription ERROR: {e}")
        text = ""
    return jsonify({"text": text})

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    audio_path = voice.speak(text)
    return send_file(audio_path, mimetype="audio/mpeg")

@app.route("/clear", methods=["POST"])
def clear():
    bot.clear_history()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)