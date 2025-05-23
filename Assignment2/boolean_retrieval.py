import json
import os
import re

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
This function performs a simple boolean AND search on the inverted index.
"""
def boolean_and_search(index, query):
    query_words = re.findall(r'\w+', query.lower())

    if not query_words:
        return []

    # Start with the doc list of the first query word
    first_word = query_words[0]
    if first_word not in index:
        return []

    result_docs = set(index[first_word].keys())

    # Intersect with other word results
    for word in query_words[1:]:
        if word in index:
            result_docs &= set(index[word].keys())
        else:
            return []  # If any word isn't in the index, no doc will match all

    return sorted(result_docs)


"""
Main function to load the index and handle user input.
"""
if __name__ == "__main__":
    index = load_index()

    while True:
        query = input("Please enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        results = boolean_and_search(index, query)
        if results:
            print("Relevant results are:", ", ".join(results))
        else:
            print("No documents matched your query.")