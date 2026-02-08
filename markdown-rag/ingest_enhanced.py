#!/usr/bin/env python3
"""
Enhanced document ingestion with PDF, web scraping, and smart chunking
"""
import os
import chromadb
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
import trafilatura
import requests
from datetime import datetime

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Split text into overlapping chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(text)

def load_markdown(file_path):
    """Load markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf(file_path):
    """Load PDF file"""
    text = ""
    with open(file_path, 'rb') as f:
        pdf_reader = pypdf.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

def scrape_webpage(url):
    """Scrape content from webpage"""
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text if text else ""
    except Exception as e:
        print(f"  ⚠️  Error scraping {url}: {e}")
        return ""

def ingest_documents(
    markdown_dir="data/markdown",
    pdf_dir="data/pdf",
    urls_file="data/urls.txt",
    collection_name="markdown_kb",
    chunk_size=1000,
    chunk_overlap=200
):
    """Enhanced ingestion with chunking and multiple formats"""
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection and create fresh
    try:
        client.delete_collection(collection_name)
        print(f"♻️  Deleted existing collection")
    except:
        pass
    
    collection = client.create_collection(collection_name)
    print(f"✨ Created fresh collection: {collection_name}\n")
    
    documents = []
    metadatas = []
    ids = []
    doc_id = 0
    
    # Process Markdown files
    print("📝 Processing Markdown files...")
    markdown_path = Path(markdown_dir)
    if markdown_path.exists():
        md_files = list(markdown_path.glob("**/*.md"))
        for md_file in md_files:
            content = load_markdown(md_file)
            chunks = chunk_text(content, chunk_size, chunk_overlap)
            
            for chunk_idx, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "filename": md_file.name,
                    "path": str(md_file),
                    "type": "markdown",
                    "chunk": chunk_idx,
                    "total_chunks": len(chunks),
                    "source": str(md_file)
                })
                ids.append(f"doc_{doc_id}")
                doc_id += 1
            
            print(f"  ✅ {md_file.name} ({len(chunks)} chunks)")
    
    # Process PDF files
    print("\n📄 Processing PDF files...")
    pdf_path = Path(pdf_dir)
    if pdf_path.exists():
        pdf_files = list(pdf_path.glob("**/*.pdf"))
        for pdf_file in pdf_files:
            content = load_pdf(pdf_file)
            chunks = chunk_text(content, chunk_size, chunk_overlap)
            
            for chunk_idx, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "filename": pdf_file.name,
                    "path": str(pdf_file),
                    "type": "pdf",
                    "chunk": chunk_idx,
                    "total_chunks": len(chunks),
                    "source": str(pdf_file)
                })
                ids.append(f"doc_{doc_id}")
                doc_id += 1
            
            print(f"  ✅ {pdf_file.name} ({len(chunks)} chunks)")
    
    # Process web URLs
    print("\n🌐 Processing web URLs...")
    urls_path = Path(urls_file)
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for url in urls:
            print(f"  Scraping: {url}")
            content = scrape_webpage(url)
            if content:
                chunks = chunk_text(content, chunk_size, chunk_overlap)
                
                for chunk_idx, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "filename": url.split('/')[-1] or "webpage",
                        "path": url,
                        "type": "web",
                        "chunk": chunk_idx,
                        "total_chunks": len(chunks),
                        "source": url
                    })
                    ids.append(f"doc_{doc_id}")
                    doc_id += 1
                
                print(f"  ✅ {url} ({len(chunks)} chunks)")
            else:
                print(f"  ❌ Failed to scrape {url}")
    
    # Add all to ChromaDB
    if documents:
        print(f"\n💾 Adding {len(documents)} chunks to ChromaDB...")
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Successfully ingested {len(documents)} total chunks!")
        print(f"   From {len(set(m['source'] for m in metadatas))} unique sources")
    else:
        print("⚠️  No documents found to ingest")
    
    return collection

if __name__ == "__main__":
    # Create data directories if they don't exist
    Path("data/markdown").mkdir(parents=True, exist_ok=True)
    Path("data/pdf").mkdir(parents=True, exist_ok=True)
    
    # Create sample urls.txt if it doesn't exist
    if not Path("data/urls.txt").exists():
        with open("data/urls.txt", 'w') as f:
            f.write("# Add URLs to scrape, one per line\n")
            f.write("# Example:\n")
            f.write("# https://docs.anthropic.com/en/api/getting-started\n")
    
    ingest_documents()
