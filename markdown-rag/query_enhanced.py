#!/usr/bin/env python3
"""
Enhanced query with source citations
"""
import os
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv('../.env')

def query_with_sources(question, n_results=5):
    """Query with detailed source citations"""
    
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("markdown_kb")
    
    print(f"\n🔍 Searching: '{question}'")
    print("=" * 70)
    
    # Search
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    # Show sources
    print(f"\n📚 Retrieved {len(documents)} relevant chunks:\n")
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        similarity = (1 - dist) * 100
        source_type = meta['type'].upper()
        chunk_info = f"chunk {meta['chunk']+1}/{meta['total_chunks']}"
        
        print(f"{i+1}. [{source_type}] {meta['filename']} ({chunk_info})")
        print(f"   Similarity: {similarity:.1f}%")
        print(f"   Source: {meta['source']}")
        print(f"   Preview: {doc[:150]}...")
        print()
    
    # Build context with citations
    context_parts = []
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        citation = f"[Source {i+1}: {meta['filename']}, {meta['type']}]"
        context_parts.append(f"{citation}\n{doc}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Prompt for Claude
    prompt = f"""Based on the following context from my documentation, please answer this question. When referencing information, please cite the source number (e.g., "According to Source 1...").

Question: {question}

Context:
{context}

Please provide a comprehensive answer with source citations."""
    
    print("💭 Asking Claude with context...\n")
    print("=" * 70)
    
    # Query Claude
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    answer = message.content[0].text
    
    print(f"\n🤖 Answer:\n")
    print(answer)
    print("\n" + "=" * 70)
    
    # Return both answer and sources for web interface
    return {
        "answer": answer,
        "sources": [
            {
                "filename": meta['filename'],
                "type": meta['type'],
                "source": meta['source'],
                "chunk": f"{meta['chunk']+1}/{meta['total_chunks']}",
                "similarity": f"{(1-dist)*100:.1f}%",
                "preview": doc[:200]
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]
    }

def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "=" * 70)
    print("📖 Enhanced Knowledge Base - RAG Query System")
    print("=" * 70)
    print("\nFeatures: PDF support, web scraping, smart chunking, source citations")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        question = input("❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not question:
            continue
        
        try:
            query_with_sources(question)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        query_with_sources(question)
    else:
        interactive_mode()
