from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)
CSV_FILE = "BooksDatasetClean.csv"

# ---------- HELPER FUNCTIONS ----------
def read_books():
    books = []
    if not os.path.exists(CSV_FILE):
        return books
    with open(CSV_FILE, mode='r', encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned = {k.strip(): v.strip() for k, v in row.items()}
            books.append(cleaned)
    return books

def save_books(books):
    headers = [
        "Title", "Authors", "Description", "Category", "Publisher",
        "Publish Date (Month)", "Publish Date (Year)", "quantity_available"
    ]
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(books)

# ---------- ROUTES ----------
@app.route('/api/books', methods=['GET'])
def get_books():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    books = read_books()
    total = len(books)
    start = (page - 1) * limit
    end = start + limit
    return jsonify({
        "books": books[start:end],
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route('/api/count', methods=['GET'])
def get_count():
    return jsonify({"total": len(read_books())})

@app.route('/api/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '').lower().strip()
    if not query:
        return jsonify([])

    stop_words = {
        "a", "an", "the", "of", "in", "from", "for", "on", "and", "to", "suggest", "give", "me", "show",
        "book", "books", "about", "some", "summary", "find", "who", "what", "where", "when", "why", "how",
        "is", "are", "was", "were", "do", "does", "did", "can", "could", "would",
        "many", "much", "copies", "copy", "available", "availability", "have", "has", "quantity", "stock",
        "tell", "please", "this", "it", "there", "any"
    }

    clean_query = query.replace('?', '').replace('!', '').replace('.', '').replace('"', '').replace("'", " ")
    query_words = [w for w in clean_query.split() if w not in stop_words and len(w) > 1]

    scored_results = []
    for row in read_books():
        title = row.get("Title", "").lower()
        author = row.get("Authors", "").lower()
        category = row.get("Category", "").lower()
        desc = row.get("Description", "").lower()

        score = 0
        if len(title) > 2 and title in query:
            score += 50

        if query_words:
            for word in query_words:
                if word in title: score += 10
                elif word in author: score += 5
                elif word in category: score += 3
                elif word in desc: score += 1
        elif query in title or query in desc:
            score += 1

        if score > 0:
            scored_results.append((score, row))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [row for _, row in scored_results[:20]]
    return jsonify(results)

@app.route('/api/save', methods=['POST'])
def save_books_endpoint():
    data = request.json.get('books', [])
    if not data:
        return jsonify({"error": "No data provided"}), 400
    save_books(data)
    return jsonify({"message": "CSV updated successfully"})

@app.route('/api/add', methods=['POST'])
def add_book():
    new_book = request.json
    books = read_books()
    books.append(new_book)
    save_books(books)
    return jsonify({"message": "Book added successfully"})

@app.route('/api/delete', methods=['POST'])
def delete_book():
    title = request.json.get("Title", "").strip()
    books = read_books()
    books = [b for b in books if b.get("Title", "").strip() != title]
    save_books(books)
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)