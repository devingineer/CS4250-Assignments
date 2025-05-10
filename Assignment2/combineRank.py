import networkx as nx
import BM25
import csv
from pageRank import build_link_graph


def combine_scores(query):
    pagerank_scores = {}
    try:
        with open("../Output/report2.csv", "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for page, score in reader:
                pagerank_scores[page] = float(score)
    except FileNotFoundError:
        print("pagerank not found, calulating pagerank")
        link_graph, url_map = build_link_graph("Repository")
        G = nx.DiGraph()

        for source, targets, in link_graph.items():
            for target in targets:
                G.add_edge(source, target)

        pagerank_scores = nx.pagerank(G, alpha=1)

    index = BM25.load_index()
    doc_lengths, avg_dl, total_num_docs = BM25.build_doc_stats(index)
    idf = BM25.compute_idf(index, total_num_docs)
    bm25_results = BM25.bm25_score(query,index, idf,doc_lengths, avg_dl)

    bm25_dict = dict(bm25_results)

    url_map = {}
    try:
        with open("FrenchOutput.txt", "r") as f:
            for i, line in enumerate(f):
                url = line.strip()
                filename = f"{i}"
                url_map[filename] = url
    except FileNotFoundError:
        print("url mapping not found")
        return []

    combined_scores = {}
    for doc_id, bm25_score in bm25_dict.items():
        if doc_id in url_map:
            url = url_map[doc_id]
            if url in pagerank_scores:
                combined_scores[doc_id] = bm25_score*pagerank_scores[url]
            else:
                combined_scores[doc_id] = bm25_score # if no url use pagerank
        else:
            combined_scores[doc_id] = bm25_score

    sorted_results = sorted(combined_scores.items(), key=lambda x:x[1], reverse=True)
    return sorted_results

if __name__ == "__main__":
    while(True):
        query = input("Please enter query or exit to leave program: ").strip()
        if query.lower() == "exit":
            break
        results = combine_scores(query)

        if results:
            print("results: ")
            for doc, score in results:
                print(f"{doc}: {score:}")
        else:
            print("no mathcing docs")