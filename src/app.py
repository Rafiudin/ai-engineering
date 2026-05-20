import streamlit as st
from openai import OpenAI
from groq import Groq
from google import genai
from core.config import config

def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "OpenAI":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
    elif provider == "Groq":
        client = Groq(api_key=config.GROQ_API_KEY)
    else:
        client = genai.Client(api_key=config.GOOGLE_API_KEY)

    if provider == "OpenAI":
        return client.chat.completions.create(
            model=model_name, 
            messages=messages, 
            max_completion_tokens=max_tokens, 
            reasoning_effort="minimal"
        ).choices[0].message.content
    elif provider == "Groq":
        return client.chat.completions.create(
            model=model_name, 
            messages=messages, 
            max_completion_tokens=max_tokens,
        ).choices[0].message.content
    else:
        return client.models.generate_content(
            model=model_name, 
            contents=[messages["content"] for messages in messages],
        ).text
    

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
        response = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = response
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({"role":"assistant","content":answer})