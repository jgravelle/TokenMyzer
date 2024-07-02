import streamlit as st
from src.utils.text_processors import preprocess_text, remove_articles, count_tokens
import logging

logger = logging.getLogger(__name__)

class TokenMyzerUI:
    def __init__(self, api):
        self.api = api
        if 'sent_tokens' not in st.session_state:
            st.session_state.sent_tokens = 0
        if 'received_tokens' not in st.session_state:
            st.session_state.received_tokens = 0
        if 'previous_total_tokens' not in st.session_state:
            st.session_state.previous_total_tokens = 0
        if 'request_count' not in st.session_state:
            st.session_state.request_count = 0

    def run(self):
        st.title("TokenMyzer")
        self._render_sidebar()
        self._render_main_content()
        self._add_download_button()

    def _render_sidebar(self):
        st.sidebar.header("Options")
        st.session_state.remove_articles = st.sidebar.checkbox("Tarzanifier")
        st.session_state.preprocess = st.sidebar.checkbox("Clean-Up")
        st.session_state.be_concise = st.sidebar.checkbox("Be Concise")

    def _render_main_content(self):
        models = self._get_models()
        if models:
            selected_model_id = self._render_model_selector(models)
            user_input = st.text_area("Enter your text here:")

            if st.button("Submit"):
                self._process_request(user_input, selected_model_id)
        else:
            st.error("Unable to fetch models. Please check your API key and connection.")

    def _get_models(self):
        logger.info("Attempting to get models in UI")
        models = self.api.get_models()
        if models and hasattr(models, 'data'):
            logger.info(f"Successfully got models in UI: {models.data}")
            return models.data
        else:
            logger.error("Failed to get models or models data is missing")
            return None

    def _render_model_selector(self, models):
        model_options = [f"{model.id} - {model.owned_by} (Context: {model.context_window})" for model in models]
        selected_model_option = st.selectbox("Select Model", model_options)
        return selected_model_option.split(' - ')[0]

    def _process_request(self, user_input, selected_model_id):
        if st.session_state.request_count > 0:
            st.session_state.previous_total_tokens = st.session_state.sent_tokens + st.session_state.received_tokens
        
        processed_input = self._process_input(user_input)
        
        st.session_state.sent_tokens = count_tokens(processed_input)
        response = self.api.chat_completion(selected_model_id, processed_input)
        if response:
            response_text = response.choices[0].message.content
            st.session_state.received_tokens = response.usage.completion_tokens
            st.write(response_text)
        else:
            st.error("Failed to get a response from the API.")

        st.session_state.request_count += 1

    def _process_input(self, text):
        if st.session_state.remove_articles:
            text = remove_articles(text)
        if st.session_state.preprocess:
            text = preprocess_text(text)
        if st.session_state.be_concise:
            text += " Be concise."
        
        if st.session_state.remove_articles or st.session_state.preprocess or st.session_state.be_concise:
            st.text("Processed input:")
            st.text(text)
        
        return text

    def _update_sidebar(self):
        st.sidebar.header("Token Information")
        st.sidebar.write(f"Sent Tokens: {st.session_state.sent_tokens}")
        st.sidebar.write(f"Received Tokens: {st.session_state.received_tokens}")
        current_total = st.session_state.sent_tokens + st.session_state.received_tokens
        st.sidebar.write(f"Total Tokens: {current_total}")
        st.sidebar.write(f"Previous Total Tokens: {st.session_state.previous_total_tokens}")

    def _add_download_button(self):
        # Implementation for download button
        pass