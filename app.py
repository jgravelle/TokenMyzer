import streamlit as st
from src.ui.streamlit_ui import TokenMyzerUI
from src.api.groq_api import GroqAPI
from config.config import load_config

def main():
    config = load_config()
    api = GroqAPI(config)
    ui = TokenMyzerUI(api)
    ui.run()

if __name__ == "__main__":
    main()