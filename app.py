import streamlit as st
from src.ui.streamlit_ui import TokenMyzerUI
from src.api.groq_api import GroqAPI
from config.config import load_config

def main():
    st.set_page_config(page_title="TokenMyzer", page_icon="🔤", layout="wide")
    
    config = load_config()
    api = GroqAPI(config)
    
    if api.client:
        ui = TokenMyzerUI(api)
        ui.run()
    else:
        st.error("Failed to initialize the Groq API client. Please check your API key and try again.")

if __name__ == "__main__":
    main()