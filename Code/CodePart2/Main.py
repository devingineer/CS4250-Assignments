import os
from Tokenizer import tokenize_document
from Stemmer import stem_tokens

# Path to the input repository folders
input_dir = os.path.join(os.getcwd(), "Code", "CodePart1", "Repository")

# Path to the output repository folders
output_dir = os.path.join(os.getcwd(), "Code", "CodePart2", "Repository")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate through each repository folder in the input directory
for repo in os.listdir(input_dir):
    repo_path = os.path.join(input_dir, repo)
    
    # Skip if it's not a directory
    if not os.path.isdir(repo_path):
        continue
    
    # Create the corresponding output repository folder
    output_repo_path = os.path.join(output_dir, repo)
    os.makedirs(output_repo_path, exist_ok=True)

    # Iterate through each HTML file in the repository folder
    for filename in os.listdir(repo_path):
        file_path = os.path.join(repo_path, filename)
        
        # Process only HTML files
        if filename.endswith(".html"):
            with open(file_path, "r", encoding="utf-8") as handle:
                # Tokenize the content of the HTML file
                tokenized_words = tokenize_document(handle.read())

                # Stem the tokenized words
                stemmed_words = stem_tokens(tokenized_words)

                # Save the stemmed output to a new file
                base_filename = os.path.splitext(filename)[0]  # Remove extension from filename
                output_path = os.path.join(output_repo_path, f"{base_filename}-StemmedOutput.txt")
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(stemmed_words))  # Write all stemmed words to the file

print("Tokenization and stemming completed. Output saved to:", output_dir)