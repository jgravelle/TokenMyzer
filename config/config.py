import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "api_key": os.getenv("GROQ_API_KEY"),
        "api_url": "https://api.groq.com/openai/v1/models"
    }