import os
import matplotlib.pyplot as plt

# Path to the input repository folders (stemmed files)
input_dir = os.path.join(os.getcwd(), "Code", "CodePart2", "Repository")

# Path to the output directory for Heaps' Law graphs
output_dir = os.path.join(os.getcwd(), "Code", "CodePart3", "ZipfGraphs")
output_dir_csv = os.path.join(os.getcwd(), "Output")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to analyze Zipf's Law for a list of files
def analyze_zipf(file_paths, output_image_path, csv_output_path, repo_name):
    word_freq = {}
    total_words = 0

    # Read and count word frequencies
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                total_words += 1
                if line in word_freq:
                    word_freq[line] += 1
                else:
                    word_freq[line] = 1

    # Sort by frequency in descending order
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    ranks = list(range(1, len(sorted_words) + 1))
    probabilities = [freq / total_words for _, freq in sorted_words]
    freq = []

    # Save word frequency data to CSV
    file_path = os.path.join(output_dir_csv, f"Words{repo_name}.csv")
    with open(file_path, 'w', encoding='utf-8') as file:
        i = 0
        for element in word_freq.values():
            if i < 50:
                outText = (f"{list(word_freq.keys())[i]}, frequency : {element}, r: {i+1}, "
                           f"Pr(%): {list(word_freq.values())[i]/total_words:.4f}, "
                           f"rPr: {((i+1) * list(word_freq.values())[i]/total_words):.4f}\n")
                print(outText)
                file.write(outText)
            i += 1
            freq.append(element)

    # Zipf's Law Plot
    plt.figure(figsize=(10, 6))
    
    # Zipf Distribution
    Zipf = [None]
    Zipf += [.1/x for x in range(1, len(sorted_words))]
    plt.plot(Zipf, label='Zipf', ls=':')
    
    plt.plot(ranks, probabilities, label=f"Crawl {repo_name}", color="blue")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Rank")
    plt.ylabel("Probability")
    plt.title(f"Zipf's Law for {repo_name} Repository")
    plt.legend()
    
    # Save the plot as an image
    plt.savefig(output_image_path)
    plt.close()

# Iterate through each repository folder in the input directory
for repo in os.listdir(input_dir):
    repo_path = os.path.join(input_dir, repo)
    
    if not os.path.isdir(repo_path):
        continue
    
    # Collect all stemmed output files in the repository folder
    file_paths = [os.path.join(repo_path, filename) for filename in os.listdir(repo_path) if filename.endswith("-StemmedOutput.txt")]
    
    # Define the output image and CSV paths
    output_image_path = os.path.join(output_dir, f"{repo}-ZipfGraph.png")
    csv_output_path = os.path.join(output_dir, f"{repo}-Words.csv")
    
    # Analyze Zipf's Law, save the graph and CSV report
    analyze_zipf(file_paths, output_image_path, csv_output_path, repo)

print("Zipf's Law analysis completed. Graphs and CSV reports saved to:", output_dir)