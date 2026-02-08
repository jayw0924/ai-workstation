import chromadb

# Initialize ChromaDB
client = chromadb.Client()

# Create a collection
collection = client.create_collection("test_collection")

# Add some documents
collection.add(
    documents=["This is a test document", "Another test document"],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_texts=["test"],
    n_results=2
)

print("ChromaDB working! Results:", results)
