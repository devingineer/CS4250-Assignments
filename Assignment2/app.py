from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, json, math, re
from collections import defaultdict
from boolean_retrieval import boolean_and_search
from BM25 import build_doc_stats, compute_idf, bm25_score
from combined_rank import load_url_map, load_pagerank_scores, combine_bm25_with_pagerank

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

"""
This function loads the inverted index from a JSON file.
"""
def load_index(json_filename="inverted_index.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, json_filename)

    with open(json_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    return index

# Load index once when app starts
index = load_index()

# Routes
@app.route("/")
def home():
    return render_template("Index.html", title="Home")

@app.route("/boolean", methods=["GET", "POST"])
def boolean_search():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form["query"]
        results = boolean_and_search(index, query)
    return render_template("Boolean.html", title="Boolean Search", query=query, results=results)

@app.route("/bm25", methods=["GET", "POST"])
def bm25_search():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form["query"]
        doc_lengths, avg_dl, total_num_docs = build_doc_stats(index)
        idf = compute_idf(index, total_num_docs)
        results = bm25_score(query, index, idf, doc_lengths, avg_dl)
    return render_template("BM25.html", title="BM25 Search", query=query, results=results)

@app.route("/api")
def api_root():
    return jsonify({"message": "Welcome to the Retrieval Search API!"})

@app.route("/api/index", methods=["GET"])
def inverted_index_api():
    return jsonify(index)

@app.route("/api/boolean", methods=["GET", "POST"])
def boolean_api():
    if request.method == "POST":
        data = request.get_json()
        query = data.get("query", "")
    else:
        query = request.args.get("query", "")
    
    results = boolean_and_search(index, query)
    return jsonify(results)

@app.route("/api/bm25", methods=["GET", "POST"])
def bm25_api():
    if request.method == "POST":
        data = request.get_json()
        query = data.get("query", "")
    else:
        query = request.args.get("query", "")
    
    doc_lengths, avg_dl, total_num_docs = build_doc_stats(index)
    idf = compute_idf(index, total_num_docs)
    results = bm25_score(query, index, idf, doc_lengths, avg_dl)
    return jsonify(results)

@app.route("/api/combined-rank", methods=["GET", "POST"])
def combined_rank_api():
    if request.method == "POST":
        data = request.get_json()
        query = data.get("query", "")
    else:
        query = request.args.get("query", "")

    doc_lengths, avg_dl, total_docs = build_doc_stats(index)
    idf = compute_idf(index, total_docs)
    bm25_results = bm25_score(query, index, idf, doc_lengths, avg_dl)

    url_map = load_url_map()
    pagerank_scores = load_pagerank_scores()
    combined_results = combine_bm25_with_pagerank(bm25_results, pagerank_scores, url_map)

    return jsonify([
        {"doc_id": doc_id, "url": url, "score": score}
        for doc_id, url, score in combined_results
    ])


if __name__ == "__main__":
    app.run(debug=True)