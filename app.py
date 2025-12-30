# app.py
import streamlit as st
from llm_connector import get_response
from mem0_handler import mem0_client

st.set_page_config(page_title="Memory Chatbot", layout="wide")
st.title("AI Chatbot")

USER_ID = "default_user"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear memory and chat button
if st.button("Clear Memory & Conversation"):
    mem0_client.delete_all(filters={"user_id": USER_ID})
    st.session_state.chat_history = []

# Container for chat messages
chat_container = st.container()

# Input box for user
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    submit_button = st.form_submit_button("Send")

# Handle user input
if submit_button and user_input:
    # First, append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Then get bot response
    bot_reply = get_response(USER_ID, user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# Display chat
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f"<div style='text-align: right; background-color:rgba(102, 187, 106, 0.8); color:white; padding:8px; margin:5px; border-radius:8px; display:inline-block;'>{chat['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align: left; background-color:rgba(28, 28, 28, 0.85); color:white; padding:8px; margin:5px; border-radius:8px; display:inline-block;'>{chat['content']}</div>",
                unsafe_allow_html=True
            )
