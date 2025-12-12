import chromadb
from chromadb.config import Settings
import os

# Define persistence directory
PERSIST_DIRECTORY = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_vector_store():
    """
    Initialize and return the ChromaDB client/collection.
    """
    # Create valid directory for chroma
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
    
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    
    # You might want to use a specific embedding function here
    # from chromadb.utils import embedding_functions
    # google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="YOUR_API_KEY")
    
    # Create or get a collection
    collection = client.get_or_create_collection(name="agent_memory")
    return collection

def add_documents(documents: list, ids: list, metadatas: list = None):
    collection = get_vector_store()
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def query_documents(query_texts: list, n_results: int = 2):
    collection = get_vector_store()
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    # Test initialization
    print(f"Initializing Vector Store in {PERSIST_DIRECTORY}...")
    col = get_vector_store()
    print(f"Collection '{col.name}' ready.")
