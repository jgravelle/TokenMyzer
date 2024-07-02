import streamlit as st
from src.ui.streamlit_ui import TokenMyzerUI
from src.api.groq_api import GroqAPI

def main():
    st.set_page_config(page_title="TokenMyzer", page_icon="🔤", layout="wide")
    
    if 'api' not in st.session_state:
        st.session_state.api = GroqAPI()

    if 'show_api_input' not in st.session_state:
        st.session_state.show_api_input = True

    if st.session_state.show_api_input:
        api_key = st.text_input("Please enter your Groq API key:", type="password", key="api_key_input")
        if api_key:
            st.session_state.api.set_api_key(api_key)
            st.session_state.show_api_input = False
            st.rerun()

    if not st.session_state.api.client or not st.session_state.get('api_key_valid', False):
        st.warning("Please enter a valid Groq API key to use the app.")
        st.session_state.show_api_input = True
    
    if st.session_state.api.client and st.session_state.get('api_key_valid', False):
        ui = TokenMyzerUI(st.session_state.api)
        ui.run()
    elif st.session_state.get('api_key_valid') == False:
        st.error("The provided API key is invalid. Please enter a valid Groq API key.")
        if st.button("Clear API Key"):
            st.session_state.api.clear_api_key()
            st.session_state.show_api_input = True
            st.rerun()

if __name__ == "__main__":
    main()