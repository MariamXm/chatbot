import streamlit as st
from llm_connector import get_response
from memory_handler import clear_user_memory_json
from mem0_handler import clear_user_memory_mem0

st.set_page_config(page_title="Persistent Memory Chatbot", layout="wide")
st.title("Persistent Memory Chatbot")

USER_ID = "mariam_user"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Clear Memory & Conversation"):
    clear_user_memory_json(USER_ID)
    clear_user_memory_mem0(USER_ID)
    st.session_state.chat_history = []

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    send = st.form_submit_button("Send")

if send and user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    bot_reply = get_response(USER_ID, user_input)
    st.session_state.chat_history.append({"role":"assistant","content":bot_reply})

for chat in st.session_state.chat_history:
    if chat["role"]=="user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Bot:** {chat['content']}")
