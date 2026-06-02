import streamlit as st
import requests
from chatbot_ui.core.config import config

def api_call(method, url, **kwargs):

    def show_error_message(message):
        """Show error message as a popup in top right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }

    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid JSON response from server."}
            
        if response.ok:
            return True, response_data
            
        return False, response_data
        
    except requests.exceptions.ConnectionError:
        show_error_message("Failed to connect to the server. Please check your connection and try again.")
        return False, {"message": "Connection error. Please try again later."}
    except requests.exceptions.Timeout:
        show_error_message("The request timed out. Please try again later.")
        return False, {"message": "Request timed out. Please try again later."}
    except requests.exceptions.RequestException as e:
        show_error_message(f"An error occurred: {str(e)}")
        return False, {"message": str(e)}

## Sidebar for model selection with streamlit
with st.sidebar:
    st.title("LLM Provider & Model Selection")
    provider = st.selectbox("Select LLM Provider", ["OpenAI", "Groq", "Google"])
    if provider == "OpenAI":
        model_name = st.selectbox("Select OpenAI Model", ["gpt-5-nano", "gpt-5-mini"])
    elif provider == "Groq":
        model_name = st.selectbox("Select Groq Model", ["llama-3.3-70b-versatile"])
    else:
        model_name = st.selectbox("Select Google Model", ["gemini-2.5-flash"])

    st.session_state.provider = provider
    st.session_state.model_name = model_name

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hello! I'm your AI assistant. How can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = api_call("post", f"{config.API_URL}/chat", json={
            "provider": st.session_state.provider,
            "model_name": st.session_state.model_name,
            "messages": st.session_state.messages
        })
        response_data = response[1]
        answer = response_data["response"]
        st.write(answer)
    st.session_state.messages.append({"role":"assistant","content":answer})