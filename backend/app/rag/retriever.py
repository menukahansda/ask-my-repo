from app.db.vectorstore import collection
from app.ingest.embed import embed

def retrieve(query, n_results=5):
    query_embedding = embed([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results