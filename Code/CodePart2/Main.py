import os
from Tokenizer import tokenize_document
from Stemmer import stem_tokens

# Update this path to the actual folder containing HTML files
directory = os.path.join(os.getcwd(), "Code", "CodePart2", "ExamplePage")

# Ensure output directories exist
output_dir = os.path.join(os.getcwd(), "Code", "CodePart2", "Output")
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Process only HTML files
    if file_path.endswith(".html"):
         with open(file_path, "r", encoding="utf-8") as handle:
                # Tokenize
                tokenized_words = tokenize_document(handle.read())

                # Stemming
                stemmed_words = stem_tokens(tokenized_words) # Apply stemming to the full list

                # Save output
                base_filename = os.path.splitext(filename)[0] # Remove extension from filename
                output_path = os.path.join(output_dir, f"{base_filename}-StemmedOutput.txt")
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(stemmed_words))  # Write all words at once