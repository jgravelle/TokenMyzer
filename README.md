# TokenMyzer

TokenMyzer is a Streamlit-based application designed to optimize text input for AI language models. It provides text preprocessing options to reduce token usage and improve efficiency in AI interactions.


## Directory Structure

TokenMyzer/
├── .gitignore
├── requirements.txt
├── README.md
├── app.py
├── config/
│   └── config.py
├── src/
│   ├── api/
│   │   └── groq_api.py
│   ├── ui/
│   │   └── streamlit_ui.py
│   ├── utils/
│   │   ├── common_words.txt
│   │   ├── helpers.py
│   │   └── text_processors.py
│   └── downloadable/
│       └── tokenmyzer_function.py
└── tests/
└── test_groq_api.py


## TokenMyzer Function

The `TokenMyzer()` function is available as a standalone Python function that can be easily integrated into existing AI applications.


### Usage

1. Download the `TokenMyzer.py` file from the Streamlit app's sidebar.
2. Place the file in your project directory.
3. Import and use the function in your Python script:

```python
from TokenMyzer import TokenMyzer

original_text = "This is a sample text that needs processing."
processed_text = TokenMyzer(original_text, clean=True, Tarzan=True, concise=True)
print(processed_text)
```

### Parameters

text (str): The input text to process.
clean (bool): Apply text cleaning (remove whitespace, punctuation, and convert to lowercase).
Tarzan (bool): Remove common words (articles, prepositions, etc.).
concise (bool): Append "Be concise." to the end of the text.
all (bool): Apply all processing options.

## TokenMyzer Streamlit App
### Setup

1.  Clone the repository:
Copygit clone https://github.com/yourusername/TokenMyzer.git
cd TokenMyzer

2.  Create a virtual environment:
Copypython -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.  Install the required packages:
Copypip install -r requirements.txt

4.  Set up your Groq API key:

5.  Create a .env file in the root directory
Add your Groq API key: GROQ_API_KEY=your_api_key_here



## Running the App

### Start the Streamlit app:
- Copystreamlit run app.py

- Open your web browser and go to http://localhost:8501.

### Using the App

Select a model from the dropdown menu.
Enter your text in the input area.
Choose preprocessing options:

Tarzanifier: Removes common words.
Clean-Up: Cleans and standardizes text.
Be Concise: Appends "Be concise." to the request.


Click "Submit" to process your text and send it to the API.
View the token usage information in the sidebar.
Download the standalone TokenMyzer function using the button in the sidebar.

###Contributing
Contributions to TokenMyzer are welcome! Please feel free to submit a Pull Request.

##License
This project is licensed under the MIT License - see the LICENSE file for details.
©2024 J. Gravelle : j@gravelle.us : https://j.gravelle.us
This README provides a comprehensive guide for both the standalone TokenMyzer function and the full Streamlit application. It includes the updated directory structure, setup instructions, usage guidelines, and information about contributing to the project. You may want to add or modify sections based on specific details of your project, such as adding a "Features" section or expanding on the "Contributing" guidelines.

