import csv
import os
from BM25 import bm25_score, load_index, build_doc_stats, compute_idf

"""
This function loads the URL mapping of the crawled pages and the Repository IDs.
"""
def load_url_map(path="Output/FrenchOutput.txt"):
    url_map = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, path)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                url = line.strip()
                filename = str(i)
                url_map[filename] = url
    except FileNotFoundError:
        print(f"URL mapping file not found: {full_path}")
    return url_map


"""
This function loads the PageRank scores from a CSV file.
"""
def load_pagerank_scores(pagerank_file="Output/PageRankScoreForOnlyCrawledLinks.csv"):
    pagerank = {}
    with open(pagerank_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Page']
            pagerank[url] = float(row['PageRank'])
    return pagerank


"""
This function combines the BM25 scores with PageRank scores.
"""
def combine_bm25_with_pagerank(bm25_results, pagerank_scores, url_map):
    combined = []
    for doc_id, bm25_score in bm25_results:
        doc_key = doc_id.replace(".html", "")
        url = url_map.get(doc_key)
        pr_score = pagerank_scores.get(url, 0.0)
        combined_score = bm25_score * pr_score
        combined.append((doc_id, combined_score))
    return sorted(combined, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    index = load_index()
    doc_lengths, avg_dl, total_docs = build_doc_stats(index)
    idf = compute_idf(index, total_docs)

    url_map = load_url_map()
    pagerank_scores = load_pagerank_scores()

    while True:
        query = input("Please enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        bm25_results = bm25_score(query, index, idf, doc_lengths, avg_dl)
        final_results = combine_bm25_with_pagerank(bm25_results, pagerank_scores, url_map)

        if final_results:
            print("Top results (BM25 x PageRank):")
            for doc_id, score in final_results[:10]:
                print(f"{doc_id} ({url_map.get(doc_id, 'N/A')}): {score:.6f}")
        else:
            print("No documents matched your query.")