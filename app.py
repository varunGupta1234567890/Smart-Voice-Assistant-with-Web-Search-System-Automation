import streamlit as st
from predict import predict_intent
from actions import perform_action

import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    threading.Thread(target=speak, args=(text,)).start()

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="centered"
)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    color: white;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
.chat-row {
    display: flex;
    width: 100%;
    margin: 5px 0;
}
.chat-user {
    margin-left: auto;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 70%;
}
.chat-bot {
    margin-right: auto;
    background: #1e293b;
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 70%;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🤖 AI Voice Assistant</div>', unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for chat in st.session_state.history:
    role = chat.get("role")
    text = chat.get("text")

    if role == "user":
        st.markdown(
            f'<div class="chat-row"><div class="chat-user"> {text}</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-row"><div class="chat-bot">🤖 {text}</div></div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

command = st.text_input(" Enter command")

col1, col2 = st.columns([1, 1])

with col1:
    send_btn = st.button("Send")

with col2:
    clear_btn = st.button("Clear")

if send_btn and command.strip():

    # Save user message
    st.session_state.history.append({
        "role": "user",
        "text": command
    })

    # Get response
    intent = predict_intent(command)
    response = perform_action(intent, command)

    speak_async(response)

    # Save bot message
    st.session_state.history.append({
        "role": "bot",
        "text": response
    })

    st.rerun()

# Clear Chat
if clear_btn:
    st.session_state.history = []
    st.rerun()

st.markdown("---")
st.subheader(" Chat History")

if st.session_state.history:
    options = [
        f'{chat["role"].upper()}: {chat["text"][:50]}'
        for chat in st.session_state.history
    ]

    selected = st.selectbox("Select message", options)
    st.info(selected)
else:
    st.info("No history yet")