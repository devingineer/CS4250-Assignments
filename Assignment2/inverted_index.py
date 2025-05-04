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

    # Convert defaultdict to regular dict so it can be serialized
    def convert_to_dict(d):
        if isinstance(d, defaultdict):
            return {k: convert_to_dict(v) for k, v in d.items()}
        else:
            return d

    index_dict = convert_to_dict(index)

    # Path to save JSON in same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "inverted_index.json")
    
    # Save the index to a JSON file
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(index_dict, f, indent=2)

    # Print a small sample of the index
    for word, occurrences in list(index.items())[:5]:
        print(f"{word}: {list(occurrences.items())[:2]}")