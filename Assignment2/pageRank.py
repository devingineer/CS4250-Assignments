from bs4 import BeautifulSoup
import os
import networkx as nx
import csv

def build_link_graph(dir):
    link_graph = {}
    filesSet = set(os.listdir(dir))

    #Read original URLs into a mapping
    url_map = {}

    with open("Assignment2/Output/Report1.csv", "r") as f:
        for i, line in enumerate(f):
            url = line.strip().split(",")
            filename = f"{i}.html"
            url_map[filename] = url[0]

    for file_name in filesSet:
        path = os.path.join(dir, file_name)
        with open(path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
            links = set()
            for link in soup.find_all("a", href=True):
                href = link['href']
                links.add(href)
            link_graph[url_map[file_name]] = links #Here storing only the url

    print("Total files in directory:", len(filesSet))
    print("Total URLs in url_map:", len(url_map))

    missing_files = [fname for fname in url_map if fname not in filesSet]
    print("Missing HTML files:", missing_files)

    return link_graph, url_map


link_graph, url_map = build_link_graph("Assignment2/Repository")

# Create a directed graph in networkx
G = nx.DiGraph()

# Add edges based on the link graph
for source, targets in link_graph.items():
    for target in targets:
        G.add_edge(source, target)

pagerank_scores = nx.pagerank(G, alpha=1) # Alpha to 1 means no surfer model

#Write scores
with open("Assignment2/Output/pageRankScores.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Page", "PageRank"])
    for page, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True):
        if page in url_map.values():
            writer.writerow([page, score])
            print(f"{page}, {score}")