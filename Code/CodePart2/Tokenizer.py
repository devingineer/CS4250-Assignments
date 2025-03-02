from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re

def Tokenize(text): 
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = text.replace("\n", " ").replace("\t", " ").strip()
    text = re.sub("\s\s+" , " ", text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    words = word_tokenize(text)
    return words
