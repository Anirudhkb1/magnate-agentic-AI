# 🤖 Streamlit Chatbot

A conversational chatbot built with Python and Streamlit.

## Features

- 💬 Modern chat interface using Streamlit's `st.chat_message` and `st.chat_input`
- ⚡ Streaming (typewriter) effect for bot responses
- 🧠 Pattern-matching responses (easily swappable with an LLM API)
- 🗑️ Clear chat button in the sidebar
- 📱 Responsive, centered layout

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**.

## Upgrading to an LLM

Replace the `get_bot_response()` function in `app.py` with an API call.

### Example with OpenAI

```python
import openai

def get_bot_response(user_message: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
    )
    return response.choices[0].message.content
```

### Example with Google Gemini

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def get_bot_response(user_message: str) -> str:
    response = model.generate_content(user_message)
    return response.text
```
