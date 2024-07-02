# src/api/groq_api.py

import requests
import streamlit as st

from groq import Groq


class GroqAPI:
    def __init__(self, config):
        self.config = config
        self.client = Groq(api_key=config['api_key'])


    def chat_completion(self, model, user_input):   
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


    def get_api_key(self):
        api_key = st.text_input("Enter your GROQ_API_KEY:", type="password")
        if api_key:
            return api_key
        st.stop()


    def get_models(self):
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.config['api_url'], headers=headers)
        return response.json()  # Return the full JSON response
