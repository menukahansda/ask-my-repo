# chromadb load/create coll
import re
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def _sanitize_name(repo_slug: str) -> str:
    """Chroma collection names must be 3-63 chars, alnum/underscore/hyphen, start/end alnum."""
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", repo_slug)
    name = name.strip("-_")
    return name[:63] or "repo"


def get_collection(repo_slug: str):
    name = _sanitize_name(repo_slug)
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def clean_collection(repo_slug: str):
    name = _sanitize_name(repo_slug)
    try:
        client.delete_collection(name=name)
        print(f"ChromaDB collection '{name}' deleted.")
    except Exception:
        pass
