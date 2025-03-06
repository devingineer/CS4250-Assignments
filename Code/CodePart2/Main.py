import os
from Tokenizer import tokenize_document
from Stemmer import stem_tokens

# Update this path to the actual folder containing HTML files
directory = os.path.join(os.getcwd(), "repository", )

# Ensure output directories exist
output_dir = os.path.join(os.getcwd(), "Output", "OutputPart2")

for repo in os.listdir(directory):
    repo_path = os.path.join(directory, repo)
    for filename in os.listdir(repo_path):
        file_path = os.path.join(repo_path, filename)
        
        # Process only HTML files
        if file_path.endswith(".html"):
            with open(file_path, "r", encoding="utf-8") as handle:
                    # Tokenize
                    tokenized_words = tokenize_document(handle.read())

                    # Stemming
                    stemmed_words = stem_tokens(tokenized_words) # Apply stemming to the full list

                    # Save output
                    base_filename = os.path.splitext(filename)[0] # Remove extension from filename
                    output_repo_path = os.path.join(output_dir, repo)
                    os.makedirs(output_repo_path, exist_ok=True)
                    output_path = os.path.join(output_repo_path, f"{base_filename}-StemmedOutput.txt")
                    with open(output_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(stemmed_words))  # Write all words at once