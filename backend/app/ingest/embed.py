# embed and upsert into vectorstore
'''Use google embedding model for lightweight and faster usage'''
from google import genai
# from sentence_transformers import SentenceTransformer

from app.config import GEMINI_API_KEY
from app.ingest.chunker import walk_and_chunk_files
from app.db.vectorstore import get_collection

genai_client = genai.Client(api_key=GEMINI_API_KEY)

# model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# to embed single text, also for query retrieval
def embed(texts):
    response = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
    )
    return [e.values for e in response.embeddings]

# embed and upsert chunks into vectorstore
def embed_and_upsert(chunks, coll):
    texts = [chunk["content"] for chunk in chunks]

    embeddings = embed(texts)

    coll.upsert(
        documents=texts,
        metadatas=[chunk["metadata"] for chunk in chunks],
        ids=[chunk["id"] for chunk in chunks],
        embeddings=embeddings,
    )

def ingest(repo_dir, repo_slug):
    coll = get_collection(repo_slug)
    chunks = walk_and_chunk_files(repo_dir)
    embed_and_upsert(chunks, coll)

if __name__ == "__main__":
    ingest()