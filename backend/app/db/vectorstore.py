# chromadb load/create coll
import re

import chromadb
from chromadb.errors import NotFoundError

from app.logging_config import get_logger

client = chromadb.PersistentClient(path="./chroma_db")
logger = get_logger(__name__)


def _sanitize_name(repo_slug: str) -> str:
    """Chroma collection names must be 3-63 chars, alnum/underscore/hyphen, start/end alnum."""
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", repo_slug)
    name = name.strip("-_")
    return name[:63] or "repo"


def get_collection(repo_slug: str):
    name = _sanitize_name(repo_slug)
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def collection_has_data(repo_slug: str) -> bool:
    """Check whether a collection exists and actually has vectors in it."""
    name = _sanitize_name(repo_slug)
    try:
        coll = client.get_collection(name=name)
        return coll.count() > 0
    except NotFoundError:
        return False  # collection doesn't exist yet


def clean_collection(repo_slug: str):
    name = _sanitize_name(repo_slug)
    try:
        client.delete_collection(name=name)
        logger.info(f"ChromaDB collection '{name}' deleted.")
    except NotFoundError:
        logger.info(f"Collection '{name}' did not exist, nothing to delete.")
