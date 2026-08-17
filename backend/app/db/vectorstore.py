# chromadb load/create coll
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="embed_collections", metadata={"hnsw:space": "cosine"}
)

def clean_collection():
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
    print("ChromaDB collection cleaned.")