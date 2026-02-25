# gemini_client.py
# This file handles all communication with the Google Gemini API.
# It sets up the client and manages the chat session.

import os
from google import genai
from google.genai import types
import streamlit as st
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables from the .env file
# This is how we keep the API key secret (never hardcode it!)
load_dotenv()


def get_gemini_client():
    """
    Configures the Gemini API with your API key and returns the client.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Please create a .env file with: GEMINI_API_KEY=your_key_here"
        )
    
    # Initialize the client. It will automatically pick up the 
    # GEMINI_API_KEY environment variable.
    client = genai.Client()
    
    return client


def start_chat_session(client, history):
    """
    Starts (or resumes) a Gemini chat session using conversation history.
    """
    # 1. Define the config FIRST
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
    )

    # 2. THEN pass the config into the chat creation
    chat_session = client.chats.create(
        model='gemini-2.5-flash',   # safer stable model
        history=history,
        config=config
    )

    return chat_session


def send_message(chat_session, user_message):
    """
    Sends a user message to Gemini and returns the assistant's response text.
    
    Args:
        chat_session: Active Gemini ChatSession
        user_message: The text the user typed
    
    Returns:
        The assistant's response as a string
    """
    response = chat_session.send_message(user_message)
    return response.text