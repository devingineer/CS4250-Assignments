import math
import json
import os
import re
from collections import defaultdict

# Parameters for BM25
k1 = 1.5
b = 0.75

"""
This function loads the inverted index from a JSON file.
"""
def load_index(json_filename="inverted_index.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, json_filename)

    with open(json_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    return index


"""
This function builds document statistics such as document lengths and average document length.
"""
def build_doc_stats(index):
    doc_lengths = defaultdict(int)
    total_docs = set()

    for word, postings in index.items():
        for doc, positions in postings.items():
            doc_lengths[doc] += len(positions)
            total_docs.add(doc)

    avg_dl = sum(doc_lengths.values()) / len(doc_lengths)
    return doc_lengths, avg_dl, len(total_docs)


"""
This function computes the IDF (Inverse Document Frequency) for each term in the index.
"""
def compute_idf(index, total_docs):
    idf = {}
    for word, postings in index.items():
        df = len(postings)
        idf[word] = math.log((total_docs - df + 0.5) / (df + 0.5) + 1)
    return idf