# embed and upsert into vectorstore
from sentence_transformers import SentenceTransformer

from app.config import CLONE_DIR
from app.ingest.chunker import walk_and_chunk_files
from app.db.vectorstore import collection

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# to embed single text, also for query retrieval
def embed(texts):
    return model.encode(texts)

# embed and upsert chunks into vectorstore
def embed_and_upsert(chunks):
    texts = [chunk["content"] for chunk in chunks]

    embeddings = embed(texts)

    collection.upsert(
        documents=texts,
        metadatas=[chunk["metadata"] for chunk in chunks],
        ids=[chunk["id"] for chunk in chunks],
        embeddings=embeddings,
    )

def ingest():
    chunks = walk_and_chunk_files(CLONE_DIR)
    embed_and_upsert(chunks)

if __name__ == "__main__":
    ingest()