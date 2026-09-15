import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="static", template_folder="templates")


@app.get("/")
def index():
    return render_template("index.html")


def local_reply(message: str) -> str:
    """Provide a useful response when no model provider is configured."""
    normalized = message.lower()
    if any(greeting in normalized for greeting in ("hello", "hi", "hey")):
        return "Hello! I am Nova, your local AI assistant. Ask me about the project, Python, or JavaScript."
    if "stimulus" in normalized:
        return "Stimulus gives this interface small, focused controllers. Here, one controller manages the conversation, loading state, and message rendering."
    if "python" in normalized:
        return "The Python backend is a Flask app. Set OPENAI_API_KEY when you want to connect a hosted model; otherwise the built-in local mode keeps the demo fully runnable."
    return f"I received: \"{message}\". Add OPENAI_API_KEY to .env for a model-powered answer, or keep exploring in local demo mode."


def model_reply(messages: list[dict[str, str]]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    payload = json.dumps({"model": model, "messages": messages, "temperature": 0.7}).encode("utf-8")
    request_object = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request_object, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


@app.post("/api/chat")
def chat():
    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()
    history = body.get("history", [])

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    safe_history = [
        {"role": item["role"], "content": str(item["content"])}
        for item in history[-10:]
        if isinstance(item, dict) and item.get("role") in {"user", "assistant"} and item.get("content")
    ]
    messages = [
        {"role": "system", "content": "You are Nova, a concise and helpful assistant for a software internship project."},
        *safe_history,
        {"role": "user", "content": message},
    ]

    reply = model_reply(messages) or local_reply(message)
    return jsonify({"reply": reply, "mode": "model" if os.getenv("OPENAI_API_KEY") else "local"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
