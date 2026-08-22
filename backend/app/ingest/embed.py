# embed and upsert into vectorstore
"""Use google embedding model for lightweight and faster usage"""

import time

from google import genai
from google.genai import errors

# from sentence_transformers import SentenceTransformer
from app.config import GEMINI_API_KEY
from app.db.vectorstore import get_collection
from app.ingest.chunker import walk_and_chunk_files
from app.logging_config import get_logger

logger = get_logger(__name__)

genai_client = genai.Client(api_key=GEMINI_API_KEY)
# model = SentenceTransformer("BAAI/bge-small-en-v1.5")


EMBED_DELAY_SECONDS = 2
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 20


# to embed single text, also for query retrieval
def embed(texts):
    time.sleep(EMBED_DELAY_SECONDS)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = genai_client.models.embed_content(
                model="gemini-embedding-001",
                contents=texts,
            )
            return [e.values for e in response.embeddings]
        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < MAX_RETRIES:
                logger.warning(
                    f"Embed rate-limited (attempt {attempt}/{MAX_RETRIES}), "
                    f"waiting {RETRY_BACKOFF_SECONDS}s before retry"
                )
                time.sleep(RETRY_BACKOFF_SECONDS)
                continue
            raise


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
    logger.info(f"[{repo_slug}] chunked {len(chunks)} chunks from {repo_dir}")

    if not chunks:
        logger.warning(f"[{repo_slug}] zero chunks produced — nothing will be ingested")

    start = time.time()
    embed_and_upsert(chunks, coll)
    logger.info(f"[{repo_slug}] embed+upsert done in {time.time()-start:.2f}s")


if __name__ == "__main__":
    ingest()
