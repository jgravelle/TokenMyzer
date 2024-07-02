
import base64
import os
import streamlit as st
from src.utils.text_processors import preprocess_text, remove_articles, count_tokens

class TokenMyzerUI:
    def __init__(self, api):
        self.api = api
        self._initialize_session_state()


    def _add_download_button(self):
        # Get the path to the tokenmyzer_function.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'downloadable', 'tokenmyzer_function.py')
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            tokenmyzer_function = file.read()

        b64 = base64.b64encode(tokenmyzer_function.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="TokenMyzer.py">Download TokenMyzer() Function</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

    def _initialize_session_state(self):
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
        selected_model_id = self._render_model_selector(models)
        user_input = st.text_area("Enter your text here:")

        if st.button("Submit"):
            self._process_request(user_input, selected_model_id)

        self._update_sidebar()

    def _get_models(self):
        if not self.api.config['api_key']:
            self.api.config['api_key'] = self.api.get_api_key()

        models_data = self.api.get_models()
        if not models_data or 'data' not in models_data:
            st.error("Unable to fetch models. Please check your API key.")
            return []
        return models_data['data']

    def _render_model_selector(self, models):
        model_options = [f"{model['id']} - {model['owned_by']} (Context: {model['context_window']})" for model in models]
        selected_model_option = st.selectbox("Select Model", model_options)
        return selected_model_option.split(' - ')[0]

    def _process_request(self, user_input, selected_model_id):
        if st.session_state.request_count > 0:
            st.session_state.previous_total_tokens = st.session_state.sent_tokens + st.session_state.received_tokens
        
        processed_input = self._process_input(user_input)
        
        st.session_state.sent_tokens = count_tokens(processed_input)
        response = self.api.chat_completion(selected_model_id, processed_input)
        response_text = response.choices[0].message.content
        st.session_state.received_tokens = response.usage.completion_tokens
        st.write(response_text)

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

        # Calculate the difference
        difference = abs(current_total - st.session_state.previous_total_tokens)

        # Determine the color based on the comparison
        if current_total > st.session_state.previous_total_tokens:
            color = "red"
        elif current_total < st.session_state.previous_total_tokens:
            color = "green"
        else:
            color = "yellow"

        # Display the difference with appropriate color
        st.sidebar.markdown(f"Difference: <font color='{color}'>{difference}</font>", unsafe_allow_html=True)