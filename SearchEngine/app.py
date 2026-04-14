from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Mock Data for Search Results
MOCK_RESULTS = [
    {"title": "The Future of AI", "url": "https://example.com/ai", "snippet": "Artificial Intelligence is evolving rapidly, transforming industries and daily life."},
    {"title": "Best Coffee Shops in NYC", "url": "https://example.com/coffee", "snippet": "A curated list of the best places to grab a cup of joe in the Big Apple."},
    {"title": "Learn Python in 30 Days", "url": "https://example.com/python", "snippet": "A comprehensive guide to mastering Python programming from scratch."},
    {"title": "SpaceX Starship Updates", "url": "https://example.com/spacex", "snippet": "Latest news on the Starship development and upcoming launches."},
    {"title": "Healthy Ealing Habits", "url": "https://example.com/health", "snippet": "Tips and tricks for maintaining a balanced diet and healthy lifestyle."},
    {"title": "Top 10 Travel Destinations 2025", "url": "https://example.com/travel", "snippet": "Explore the most breathtaking locations to visit in the upcoming year."},
    {"title": "Understanding Quantum Computing", "url": "https://example.com/quantum", "snippet": "An introduction to the complex world of quantum mechanics and computing."},
    {"title": "Delicious Pasta Recipes", "url": "https://example.com/pasta", "snippet": "Authentic Italian pasta recipes that you can make at home."},
    {"title": "History of the Roman Empire", "url": "https://example.com/rome", "snippet": "A deep dive into the rise and fall of one of history's greatest empires."},
    {"title": "DIY Home Improvement Projects", "url": "https://example.com/diy", "snippet": "Fun and easy projects to upgrade your living space on a budget."}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    # Simple mock search logic
    results = [
        r for r in MOCK_RESULTS 
        if query in r['title'].lower() or query in r['snippet'].lower()
    ]
    
    # Simulate some network latency or randomness if needed, but keeping it fast for now
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
