import re
import tiktoken
import os

def load_common_words():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'common_words.txt')
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

COMMON_WORDS = load_common_words()

def preprocess_text(text):
    # Replace all whitespace characters (including line feeds) with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove punctuation (except period, question mark, and exclamation point)
    text = re.sub(r'[^\w\s.!?]', '', text)
    # Convert to lowercase
    return text.lower().strip()

def remove_articles(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in COMMON_WORDS]
    return ' '.join(filtered_words)

def count_tokens(text):
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except:
        return len(text.split())
    return len(encoding.encode(text))