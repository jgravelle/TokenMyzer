# src/api/groq_api.py

import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

class GroqAPI:
    def __init__(self):
        self.client = None
        self.initialize_client()

    def initialize_client(self):
        api_key = self.get_api_key()
        if api_key:
            self.client = Groq(api_key=api_key)
            self.test_api_key()  # Test the API key

    def get_api_key(self):
        # Try to get the API key from environment variables
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        # If not found in environment, check session state
        if not api_key and 'groq_api_key' in st.session_state:
            api_key = st.session_state.groq_api_key
        
        # If still not found, prompt the user
        if not api_key:
            api_key = st.text_input("Please enter your Groq API key:", type="password", key="api_key_input")
            if api_key:
                st.session_state.groq_api_key = api_key
        
        return api_key

    def test_api_key(self):
        try:
            self.get_models()
            st.session_state.api_key_valid = True
        except Exception:
            st.session_state.api_key_valid = False
            self.client = None  # Reset client if key is invalid

    def get_models(self):
        if not self.client:
            return None
        
        response = self.client.models.list()
        return response.json()

    def chat_completion(self, model, user_input):
        if not self.client:
            return None
        
        return self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            model=model,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=False
        )