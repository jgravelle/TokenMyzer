# src/api/groq_api.py

import streamlit as st
import requests
from groq import Groq
import os
from dotenv import load_dotenv

class GroqAPI:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.initialize_client()

    def initialize_client(self):
        api_key = self.get_api_key()
        if api_key:
            self.client = Groq(api_key=api_key)
            self.config['api_key'] = api_key
        else:
            st.error("No API key provided. The app cannot function without a valid Groq API key.")
            st.stop()

    def get_api_key(self):
        # Try to get the API key from environment variables
        load_dotenv()  # This loads the .env file if it exists
        api_key = os.getenv("GROQ_API_KEY")
        
        # If not found in environment, prompt the user
        if not api_key:
            st.warning("GROQ_API_KEY not found in environment variables.")
            api_key = st.text_input("Please enter your Groq API key:", type="password")
            if api_key:
                # Optionally, you can save this to .env file for future use
                with open(".env", "a") as env_file:
                    env_file.write(f"\nGROQ_API_KEY={api_key}")
                st.success("API key saved for this session. Restart the app to use the saved key.")
        
        return api_key

    def get_models(self):
        if not self.client:
            return None
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.config['api_url'], headers=headers)
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