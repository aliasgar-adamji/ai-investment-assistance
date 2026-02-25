# app.py
# This is the main Streamlit application.
# It handles the chat UI and session-based memory.

import streamlit as st
from gemini_client import get_gemini_client, start_chat_session, send_message

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Investment Assistant",
    page_icon="💹",
    layout="centered"
)

# ── App Title & Description ──────────────────────────────────────────────────
st.title("💹 AI Investment Decision Assistant")
st.caption("Powered by Google Gemini · For educational purposes only")
st.divider()


# ── Initialize Session State ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []

# ✅ FIXED: Changed "model" to "client" to match the new SDK terminology
if "client" not in st.session_state:
    try:
        st.session_state.client = get_gemini_client()
    except ValueError as e:
        st.error(f"⚠️ Configuration Error: {e}")
        st.stop()


# ── Display Chat History ──────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ── Handle New User Input ─────────────────────────────────────────────────────
user_input = st.chat_input("Ask me about investments, savings, or financial planning...")

if user_input:
    # 1. Show the user's message immediately in the chat
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. Save the user message to our display history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # 3. Get the assistant's response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # ✅ FIXED: Passed 'client' instead of 'model'
                chat_session = start_chat_session(
                    client=st.session_state.client,
                    history=st.session_state.gemini_history
                )
                
                # Send the new user message and get a response
                response_text = send_message(chat_session, user_input)
                
                # Display the response
                st.markdown(response_text)
                
            except Exception as e:
                response_text = f"❌ Error communicating with Gemini: {str(e)}"
                st.error(response_text)
    
    # 4. Save the assistant's response to our display history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })
    
    # 5. Update Gemini history with BOTH the user message and model response
    # ✅ FIXED: Updated the 'parts' structure to match the new SDK format [{"text": ...}]
    st.session_state.gemini_history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })
    st.session_state.gemini_history.append({
        "role": "model",
        "parts": [{"text": response_text}]
    })


# ── Sidebar: Info & Controls ──────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ About This App")
    st.markdown("""
    This is an **AI-powered financial education chatbot** built with:
    - 🤖 Google Gemini (Chat API)
    - 🖼️ Streamlit (UI)
    - 🐍 Python
    
    **What it can help with:**
    - Investment options (stocks, bonds, ETFs, mutual funds)
    - Risk assessment
    - Portfolio diversification basics
    - Savings strategies
    """)
    
    st.divider()
    
    # Show how many messages have been exchanged
    msg_count = len(st.session_state.messages)
    st.metric("Messages in conversation", msg_count)
    
    st.divider()
    
    # Button to clear the conversation and start fresh
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.gemini_history = []
        st.rerun() 
    
    st.divider()
    st.caption("⚠️ This app is for educational purposes only. Not financial advice.")