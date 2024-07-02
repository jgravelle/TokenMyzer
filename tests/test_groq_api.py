import unittest
from src.api.groq_api import GroqAPI

class TestGroqAPI(unittest.TestCase):
    def setUp(self):
        self.config = {
            "api_key": "test_key",
            "api_url": "https://api.groq.com/openai/v1/models"
        }
        self.api = GroqAPI(self.config)

    def test_get_models(self):
        # Mock the API response and test the get_models method
        pass

    def test_chat_completion(self):
        # Mock the API response and test the chat_completion method
        pass

if __name__ == '__main__':
    unittest.main()