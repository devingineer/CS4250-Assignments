from bs4 import BeautifulSoup
import re

def CleanText(text): 
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = text.replace("\n", " ").replace("\t", " ").strip()
    text = re.sub("\s\s+" , " ", text)
    
    return text
