import os
import math
import matplotlib.pyplot as plt

# Path to the input repository folders (stemmed files)
input_dir = os.path.join(os.getcwd(), "Code", "CodePart2", "Repository")

# Path to the output directory for Heaps' Law graphs
output_dir = os.path.join(os.getcwd(), "Code", "CodePart3", "HeapsGraphs")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to analyze Heaps' Law for a list of files
def analyze_heaps(file_paths, output_image_path, repo_name):
    uniqueWords = []
    vocabulary = []

    # Aggregate vocabulary growth across all files
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line not in uniqueWords:
                    uniqueWords.append(line)
                vocabulary.append(len(uniqueWords))

    # Heaps' Law Calculation
    index1 = int(len(vocabulary) * 0.3)
    index2 = int(len(vocabulary) * 0.65)
    B = (math.log(vocabulary[index1], 10) - math.log(vocabulary[index2], 10)) / (math.log(index1, 10) - math.log(index2, 10))
    k = round(vocabulary[index1] / (pow(index1, B)), 3)
    B = round(B, 3)

    print(f"Repository: {repo_name}")
    print(f"Corpus: {len(vocabulary)}, UniqueWords: {len(uniqueWords)}")
    print(f"Heaps' Values, Beta: {B}, K: {k}")

    # Heaps' Law Plot
    Heaps = [k * pow(x, B) for x in range(len(vocabulary))]
    lbl = f"Heaps' Law (k={k}, B={B})"

    plt.figure(figsize=(10, 6))
    plt.plot(Heaps, label=lbl, ls=":")
    plt.plot(vocabulary, label=f"Crawl {repo_name}", color="blue")
    plt.xlabel("Words in Collection")
    plt.ylabel("Words in Vocabulary")
    plt.title(f"Vocabulary Growth for {repo_name} Repository")
    plt.legend()
    
    # Save the plot as an image
    plt.savefig(output_image_path)
    plt.close()

# Iterate through each repository folder in the input directory
for repo in os.listdir(input_dir):
    repo_path = os.path.join(input_dir, repo)
    
    # Skip if it's not a directory
    if not os.path.isdir(repo_path):
        continue
    
    # Collect all stemmed output files in the repository folder
    file_paths = []
    for filename in os.listdir(repo_path):
        if filename.endswith("-StemmedOutput.txt"):
            file_paths.append(os.path.join(repo_path, filename))
    
    # Define the output image path
    output_image_path = os.path.join(output_dir, f"{repo}-HeapsGraph.png")
    
    # Analyze Heaps' Law for the entire repository and save the graph
    analyze_heaps(file_paths, output_image_path, repo)

print("Heaps' Law analysis completed. Graphs saved to:", output_dir)