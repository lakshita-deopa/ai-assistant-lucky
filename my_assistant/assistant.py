import requests
import sqlite3
import json
from datetime import datetime

IMAGE_KEYWORDS = ["generate", "draw", "create", "make", "paint", "image of", "picture of"]

class Assistant:
    def __init__(self):
        self.system_prompt = "You are a helpful personal AI assistant named Lucky. Be friendly, concise, and helpful."
        self.db_path = "lucky_memory.db"
        self._init_db()
        self.history = self._load_history()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _load_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM conversations ORDER BY id ASC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        return [{"role": role, "content": content} for role, content in rows]

    def _save_message(self, role: str, content: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def is_image_request(self, message: str) -> bool:
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in IMAGE_KEYWORDS)

    def extract_image_prompt(self, message: str) -> str:
        for keyword in ["generate an image of", "generate image of", "draw me a", "draw a",
                        "create an image of", "create image of", "make an image of",
                        "paint a", "picture of", "image of", "generate a"]:
            if keyword in message.lower():
                idx = message.lower().index(keyword) + len(keyword)
                return message[idx:].strip()
        return message

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        self._save_message("user", user_message)

        messages = [{"role": "system", "content": self.system_prompt}] + self.history
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        })
        reply = response.json()["message"]["content"]

        self.history.append({"role": "assistant", "content": reply})
        self._save_message("assistant", reply)

        return reply

    def clear_history(self):
        self.history = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
        return "Conversation cleared."