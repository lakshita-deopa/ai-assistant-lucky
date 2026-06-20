import whisper
import pyttsx3
import tempfile
import os

class VoiceHandler:
    def __init__(self):
        self.whisper_model = None
        self.tts_engine = None

    def load_whisper(self):
        if self.whisper_model is None:
            print("Loading Whisper model...")
            self.whisper_model = whisper.load_model("small")
            print("Whisper model loaded!")

    def transcribe(self, audio_file_path: str) -> str:
        self.load_whisper()
        result = self.whisper_model.transcribe(audio_file_path)
        return result["text"].strip()

    def speak(self, text: str) -> str:
        if self.tts_engine is None:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 175)

        temp_file = os.path.join(tempfile.gettempdir(), "lucky_speech.mp3")
        self.tts_engine.save_to_file(text, temp_file)
        self.tts_engine.runAndWait()
        return temp_file