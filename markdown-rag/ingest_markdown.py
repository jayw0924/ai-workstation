#!/usr/bin/env python3
"""
Ingest markdown files into ChromaDB for RAG
"""
import os
import chromadb
from pathlib import Path
from chromadb.config import Settings

def ingest_markdown_files(markdown_dir="data/markdown", collection_name="markdown_kb"):
    """Load all markdown files into ChromaDB"""
    
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get collection
    try:
        collection = client.get_collection(collection_name)
        print(f"Using existing collection: {collection_name}")
    except:
        collection = client.create_collection(collection_name)
        print(f"Created new collection: {collection_name}")
    
    # Find all markdown files
    markdown_path = Path(markdown_dir)
    md_files = list(markdown_path.glob("**/*.md"))
    
    print(f"\nFound {len(md_files)} markdown files")
    
    # Process each file
    documents = []
    metadatas = []
    ids = []
    
    for idx, md_file in enumerate(md_files):
        # Read file content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store document
        documents.append(content)
        metadatas.append({
            "filename": md_file.name,
            "path": str(md_file),
            "type": "markdown"
        })
        ids.append(f"doc_{idx}")
        
        print(f"  Loaded: {md_file.name}")
    
    # Add to ChromaDB
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"\n✅ Successfully ingested {len(documents)} documents into ChromaDB")
    else:
        print("⚠️  No documents found to ingest")
    
    return collection

if __name__ == "__main__":
    ingest_markdown_files()
