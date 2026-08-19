from app.db.vectorstore import get_collection
from app.ingest.embed import embed

def retrieve(query, repo_slug, n_results=5):
    coll = get_collection(repo_slug)
    query_embedding = embed([query])[0]
    results = coll.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results