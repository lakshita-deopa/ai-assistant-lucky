import requests

class Assistant:
    def __init__(self):
        self.system_prompt = "You are a helpful personal AI assistant named Lucky. Be friendly, concise, and helpful."
        self.history = []

    def chat(self, user_message: str) -> str:
        self.history.append({
            "role": "user",
            "content": user_message
        })
        messages = [{"role": "system", "content": self.system_prompt}] + self.history
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        })
        reply = response.json()["message"]["content"]
        self.history.append({
            "role": "assistant",
            "content": reply
        })
        return reply

    def clear_history(self):
        self.history = []
        return "Conversation cleared."