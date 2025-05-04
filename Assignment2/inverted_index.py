import os
import re
import json
from collections import defaultdict
from bs4 import BeautifulSoup

def build_index(pages):
    index = defaultdict(lambda: defaultdict(list))
    for url, text in pages:
        words = re.findall(r'\w+', text.lower())
        for pos, word in enumerate(words):
            index[word][url].append(pos)
    return index


def build_inverted_index_for_repo(repo_name="Repository"):
    inverted_index = defaultdict(lambda: defaultdict(list))  # word -> file -> [positions]
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), repo_name)

    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Repository not found: {base_dir}")

    for file_name in os.listdir(base_dir):
        if file_name.endswith(".html"):
            file_path = os.path.join(base_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                    text = soup.get_text()
                    words = re.findall(r'\w+', text.lower())

                    for pos, word in enumerate(words):
                        inverted_index[word][file_name].append(pos)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return inverted_index


if __name__ == "__main__":
    index = build_inverted_index_for_repo("Repository")
    
    # Save the index to a JSON file
    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    # Print a small sample of the index
    for word, occurrences in list(index.items())[:5]:
        print(f"{word}: {list(occurrences.items())[:2]}")