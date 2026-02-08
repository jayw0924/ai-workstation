#!/usr/bin/env python3
"""
Web interface for the Knowledge Base RAG system
"""
from flask import Flask, render_template, request, jsonify
import os
from query_enhanced import query_with_sources
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """Handle query requests"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        result = query_with_sources(question, n_results=5)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    """Get knowledge base statistics"""
    import chromadb
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection("markdown_kb")
        count = collection.count()
        
        return jsonify({
            'total_chunks': count,
            'collection_name': 'markdown_kb'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    Path('templates').mkdir(exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🌐 Knowledge Base Web Interface")
    print("=" * 60)
    print("\n📡 Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
