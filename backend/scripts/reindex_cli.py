from app.config import TARGET_REPO_URL
from app.db.vectorstore import clean_collection
from app.ingest.embed import ingest
from app.ingest.fetch_repo import fetch_repo


def reindex():
    result = fetch_repo(TARGET_REPO_URL)
    if not result["success"]:
        print(f"Reindex failed: {result['message']}")
        return

    try:
        clean_collection(result["repo_slug"])
        ingest(result["clone_dir"], result["repo_slug"])
    except Exception as e:
        print(f"Reindex failed during embedding: {e}")
        return

    print("Reindex completed successfully.")


if __name__ == "__main__":
    reindex()