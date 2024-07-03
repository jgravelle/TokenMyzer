import streamlit as st
from src.ui.streamlit_ui import TokenMyzerUI
from src.api.groq_api import GroqAPI
import logging

logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="TokenMyzer", page_icon="ⅉ", layout="wide")
    
    logger.info("Starting TokenMyzer app")

    if 'api' not in st.session_state:
        logger.info("Initializing GroqAPI in session state")
        st.session_state.api = GroqAPI()

    if not st.session_state.api.client or not st.session_state.get('api_key_valid', False):
        logger.info("No valid API client, prompting for API key")
        api_key = st.text_input("Please enter your Groq API key:", type="password", key="api_key_input")
        if api_key:
            logger.info("API key entered, setting in GroqAPI")
            st.session_state.api.set_api_key(api_key)
            st.rerun()
        st.warning("Please enter a valid Groq API key to use the app.")
    else:
        logger.info("Valid API client found, running TokenMyzerUI")
        ui = TokenMyzerUI(st.session_state.api)
        ui.run()

    if st.button("Clear API Key"):
        logger.info("Clearing API key")
        st.session_state.api.clear_api_key()
        st.rerun()

if __name__ == "__main__":
    main()