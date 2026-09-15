# Internship
Xtelify Internship Repository

## Nova AI chatbot

Nova is a small AI chatbot built with a Stimulus JavaScript frontend and a Python Flask backend.

### Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The app works immediately in local demo mode. To connect an OpenAI-compatible model, copy `.env.example` to `.env` and provide `OPENAI_API_KEY`, `OPENAI_MODEL`, and optionally `OPENAI_BASE_URL`.
