from app.config import TARGET_REPO_URL
from app.db.vectorstore import clean_collection
from app.ingest.embed import ingest
from app.ingest.fetch_repo import fetch_repo


def reindex():
    result = fetch_repo(TARGET_REPO_URL)
    if not result["success"]:
        print(f"Reindex failed: {result['message']}")
        return

    clean_collection(result["repo_slug"])
    ingest(result["clone_dir"], result["repo_slug"])
    print("Reindex completed successfully.")
    
if __name__ == "__main__":
    reindex()