from bs4 import BeautifulSoup
import os
import networkx as nx
import csv
import json

def build_link_graph(dir):
    link_graph = {}
    filesSet = set(os.listdir(dir))

    # Read original URLs into a mapping
    url_map = {}
    with open("Output/FrenchOutput.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            url = line.strip()
            filename = f"{i}.html"
            url_map[filename] = url

    for file_name in filesSet:
        if file_name.endswith(".html") and file_name in url_map:
            path = os.path.join(dir, file_name)
            with open(path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "html.parser")
                links = set()
                for link in soup.find_all("a", href=True):
                    href = link['href']
                    links.add(href)
                link_graph[url_map[file_name]] = links

    return link_graph, url_map


if __name__ == "__main__":
    # Build link graph
    link_graph, url_map = build_link_graph("Repository")

    # Create a directed graph in networkx
    G = nx.DiGraph()

    # Add edges based on the link graph
    for source, targets in link_graph.items():
        for target in targets:
            G.add_edge(source, target)

    # Compute PageRank
    pagerank_scores = nx.pagerank(G, alpha=1) # Alpha to 1 means no surfer model

    # Prepare output path
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "PageRankScoreForOnlyCrawledLinks.csv")
    json_path = os.path.join(output_dir, "pagerank-top100.json")

    # Write CSV
    with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Page", "PageRank"])
        for page, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True):
            if page in url_map.values():
                writer.writerow([page, score])
                print(f"{page}, {score}")

    # Write JSON (top 100)
    top_100 = [
        {"url": page, "score": score}
        for page, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
        if page in url_map.values()
    ][:100]

    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(top_100, jsonfile, indent=2)

    print(f"Top 100 PageRank scores written to:\n→ {csv_path}\n→ {json_path}")