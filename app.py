import streamlit as st
from src.ui.streamlit_ui import TokenMyzerUI
from src.api.groq_api import GroqAPI

def main():
    st.set_page_config(page_title="TokenMyzer", page_icon="🔤", layout="wide")
    
    if 'api' not in st.session_state:
        st.session_state.api = GroqAPI()

    if not st.session_state.api.client or not st.session_state.get('api_key_valid', False):
        st.warning("Please enter a valid Groq API key to use the app.")
        st.session_state.api.initialize_client()
    
    if st.session_state.api.client and st.session_state.get('api_key_valid', False):
        ui = TokenMyzerUI(st.session_state.api)
        ui.run()
    elif st.session_state.get('api_key_valid') == False:
        st.error("The provided API key is invalid. Please enter a valid Groq API key.")
        # Add a button to clear the invalid key
        if st.button("Clear API Key"):
            st.session_state.pop('groq_api_key', None)
            st.session_state.pop('api_key_valid', None)
            st.experimental_rerun()

if __name__ == "__main__":
    main()