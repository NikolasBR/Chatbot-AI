import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

st.title("Chatbot GEMINI Simplificado Para Receitas: Ingredientes e Modo de Preparo")
if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CONEXÃO COM A API
load_dotenv()
GEMINI_API_KEY = os.getenv("Gemini_API_KEY")
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error("Erro ao carregar a chave GEMINI_API_KEY.")
    st.stop()

#COMUNICAÇÃO IA
def get_gemini_response(prompt):
    history = []
    for message in st.session_state["messages"]:
        role = "model" if message["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [{"text": message["content"]}]})
    chat = client.chats.create(model="gemini-2.5-flash", history=history)
    response = chat.send_message(prompt)
    return response.text

# Lógica de Input/Output

if prompt := st.chat_input("Pergunte algo ao seu Assistente Culinário"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("A IA está pensando..."):
        response_text = get_gemini_response(prompt)
    st.session_state["messages"].append({"role": "assistent", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text) 