# src/api/groq_api.py

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqAPI:
    def __init__(self):
        self.client = None
        logger.info("Initializing GroqAPI")
        self.initialize_client()

    def initialize_client(self):
        api_key = self.get_api_key()
        if api_key:
            logger.info("API key found, attempting to initialize Groq client")
            try:
                self.client = Groq(api_key=api_key)
                self.test_api_key()
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {str(e)}")
                st.error(f"Failed to initialize Groq client: {str(e)}")
                self.client = None
        else:
            logger.warning("No API key found")

    def get_api_key(self):
        logger.info("Attempting to get API key")
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            logger.info("API key found in environment variables")
        elif 'groq_api_key' in st.session_state:
            api_key = st.session_state.groq_api_key
            logger.info("API key found in session state")
        else:
            logger.warning("No API key found in environment or session state")
        return api_key

    def set_api_key(self, api_key):
        logger.info("Setting new API key")
        st.session_state.groq_api_key = api_key
        self.initialize_client()

    def clear_api_key(self):
        logger.info("Clearing API key")
        if 'groq_api_key' in st.session_state:
            del st.session_state.groq_api_key
        if 'api_key_valid' in st.session_state:
            del st.session_state.api_key_valid
        self.client = None

    def test_api_key(self):
        logger.info("Testing API key")
        try:
            models = self.client.models.list()
            logger.info(f"API key test successful. Models: {models}")
            st.session_state.api_key_valid = True
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            st.error(f"API key validation failed: {str(e)}")
            st.session_state.api_key_valid = False
            self.client = None

    def get_models(self):
        if not self.client:
            logger.warning("Attempted to get models without initialized client")
            return None
        try:
            logger.info("Fetching models")
            models = self.client.models.list()
            logger.info(f"Successfully fetched models: {models}")
            return models
        except Exception as e:
            logger.error(f"Failed to fetch models: {str(e)}")
            st.error(f"Failed to fetch models: {str(e)}")
            return None

    def chat_completion(self, model, user_input):
        if not self.client:
            logger.warning("Attempted chat completion without initialized client")
            return None
        try:
            logger.info(f"Attempting chat completion with model: {model}")
            response = self.client.chat.completions.create(
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
            logger.info("Chat completion successful")
            return response
        except Exception as e:
            logger.error(f"Chat completion failed: {str(e)}")
            st.error(f"Chat completion failed: {str(e)}")
            return None