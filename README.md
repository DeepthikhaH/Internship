# GenAI ChatBot

A Streamlit chatbot powered by Google's Gemini API. The app keeps the conversation in the current browser session and sends the conversation history to Gemini for context-aware responses.

## Features

- Streamlit chat interface
- Gemini `gemini-3.6-flash` model integration
- Conversation history during the current session
- Clear conversation control
- Secure API key loading from environment variables or Streamlit secrets
- Ready for Streamlit Community Cloud deployment

## Project Structure

```text
.
|-- GenAI_ChatBot.py
|-- requirements.txt
|-- .streamlit/
|   |-- config.toml
|   |-- secrets.toml.example
|-- .gitignore
```

## Local Setup

1. Clone the repository and open its folder:

   ```powershell
   cd Internship
   ```

2. Create and activate a virtual environment if needed:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create `.streamlit\secrets.toml` and add your Gemini API key:

   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   ```

   Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey). Never commit `secrets.toml` or place the key in Python code.

5. Start the app:

   ```powershell
   streamlit run GenAI_ChatBot.py
   ```

   Open the local URL shown by Streamlit, usually `http://localhost:8507`.

## Environment Variable Alternative

Instead of a Streamlit secret, set the key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key"
streamlit run GenAI_ChatBot.py
```

## Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new app at [Streamlit Community Cloud](https://share.streamlit.io).
3. Select the repository, branch, and `GenAI_ChatBot.py` as the main file.
4. In the app settings, open **Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   ```

5. Save the secret and reboot the app.

Do not upload `.streamlit/secrets.toml`; it should be excluded by `.gitignore`.

## Configuration

The app listens on all network interfaces when run with the included `.streamlit/config.toml`, which allows access from other devices on the same local network. For public access, use Streamlit Community Cloud or another hosting provider.

The model can be changed with the `GEMINI_MODEL` environment variable:

```powershell
$env:GEMINI_MODEL = "gemini-3.6-flash"
```

## Security

- Revoke any API key that has been exposed in chat, source code, screenshots, or public repositories.
- Generate a replacement key and store it only in Streamlit Cloud Secrets, `.streamlit/secrets.toml`, or an environment variable.
- Never commit credentials to GitHub.
