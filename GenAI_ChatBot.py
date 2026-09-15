import os

import streamlit as st
from google import genai


st.set_page_config(
	page_title="GenAI ChatBot",
	page_icon="💬",
	layout="centered",
)


def get_api_key() -> str | None:
	"""Read the API key from the environment or Streamlit secrets."""
	api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
	if api_key:
		return api_key

	try:
		return st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
	except (FileNotFoundError, KeyError):
		return None


def generate_response(messages: list[dict[str, str]]) -> str:
	"""Generate an assistant response using the Gemini API."""
	api_key = get_api_key()
	if not api_key:
		raise RuntimeError(
			"Set GEMINI_API_KEY as an environment variable or Streamlit secret "
			"before sending a message."
		)

	conversation = "\n\n".join(
		f"{message['role'].capitalize()}: {message['content']}"
		for message in messages
	)
	client = genai.Client(api_key=api_key)
	response = client.models.generate_content(
		model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
		contents=(
			"You are a helpful, concise assistant.\n\n"
			f"Conversation:\n{conversation}"
		),
	)
	return response.text or "Gemini returned an empty response."


st.title("GenAI ChatBot 💬")
st.caption("Ask a question and start a conversation.")

if "messages" not in st.session_state:
	st.session_state.messages = []

with st.sidebar:
	st.header("Chat settings")
	st.write("Your conversation is stored only for this browser session.")
	st.caption("Model: `gemini-3.6-flash`")
	if get_api_key():
		st.success("Gemini API key loaded")
	else:
		st.warning("Gemini API key missing")
	if st.button("Clear conversation", use_container_width=True):
		st.session_state.messages = []
		st.rerun()

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

if prompt := st.chat_input("Message the chatbot..."):
	st.session_state.messages.append({"role": "user", "content": prompt})
	with st.chat_message("user"):
		st.markdown(prompt)

	try:
		with st.spinner("Thinking..."):
			response = generate_response(st.session_state.messages)
	except Exception as error:
		st.error(f"Gemini request failed: {error}")
	else:
		st.session_state.messages.append({"role": "assistant", "content": response})
		with st.chat_message("assistant"):
			st.markdown(response)