from nltk.stem import PorterStemmer

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(token) for token in tokens]
    return stemmed_words