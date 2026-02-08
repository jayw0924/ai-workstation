#!/usr/bin/env python3
"""
Query your markdown knowledge base using RAG + Claude
"""
import os
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

def query_knowledge_base(question, n_results=3):
    """Query the knowledge base and get Claude's answer"""
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("markdown_kb")
    
    print(f"\n🔍 Searching knowledge base for: '{question}'")
    print("-" * 60)
    
    # Search for relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
    # Extract relevant documents
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    print(f"\n📚 Found {len(documents)} relevant documents:\n")
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        print(f"{i+1}. {meta['filename']} (similarity: {1-dist:.2%})")
        print(f"   Preview: {doc[:100]}...")
        print()
    
    # Prepare context for Claude
    context = "\n\n---\n\n".join([
        f"From {meta['filename']}:\n{doc}" 
        for doc, meta in zip(documents, metadatas)
    ])
    
    # Build prompt for Claude
    prompt = f"""Based on the following context from my markdown documentation, please answer this question:

Question: {question}

Context:
{context}

Please provide a clear, concise answer based on the information in the context. If the context doesn't contain enough information to answer fully, please say so."""
    
    print("💭 Asking Claude...\n")
    print("=" * 60)
    
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
    
    print(f"\n🤖 Claude's Answer:\n")
    print(answer)
    print("\n" + "=" * 60)
    
    return answer

def interactive_mode():
    """Run in interactive mode for multiple queries"""
    print("\n" + "=" * 60)
    print("📖 Markdown Knowledge Base - RAG Query System")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to stop\n")
    
    while True:
        question = input("❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not question:
            continue
        
        try:
            query_knowledge_base(question)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Single query mode
        question = " ".join(sys.argv[1:])
        query_knowledge_base(question)
    else:
        # Interactive mode
        interactive_mode()
