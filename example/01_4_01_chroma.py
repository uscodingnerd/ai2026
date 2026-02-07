import chromadb
from chromadb.config import Settings

# Create a Chroma client (in-memory)
client = chromadb.Client(
    Settings(anonymized_telemetry=False)
)

# Create a collection
collection = client.create_collection(
    name="my_collection"
)

# Add documents and their embeddings (vectors)
collection.add(
    documents=[
        "Paris is the capital of France",
        "Berlin is in Germany",
        "Tokyo is in Japan"
    ],
    metadatas=[
        {"source": "wiki"},
        {"source": "wiki"},
        {"source": "wiki"}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Query with a new document
results = collection.query(
    query_texts=["What is the capital of Germany?"],
    n_results=2 # Returns the top 2 most similar documents to the query.
)
print(results)
