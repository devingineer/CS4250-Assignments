import re
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("punkt_tab")

def tokenize_document(document):
    soup = BeautifulSoup(document, "html.parser")
    for script in soup(["script", "style"]):  
        script.extract() # Remove JavaScript and CSS
    text = soup.get_text()  # Extract plain text
    
    # Keep only alphanumeric sequences
    words = word_tokenize(text)
    tokens = [word.lower() for word in words if re.match(r"^[a-zA-Z0-9]+$", word)]

    return tokens