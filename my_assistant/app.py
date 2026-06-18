from flask import Flask, request, jsonify, render_template
from assistant import Assistant

app = Flask(__name__)
bot = Assistant()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message.strip():
        return jsonify({"reply": ""})
    reply = bot.chat(user_message)
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    bot.clear_history()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)