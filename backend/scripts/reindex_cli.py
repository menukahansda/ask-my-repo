from app.config import TARGET_REPO_URL, CLONE_DIR
from app.db.vectorstore import clean_collection
from app.ingest.fetch_repo import clean_repo, fetch_repo
from app.ingest.embed import ingest

def reindex():
    clean_repo(CLONE_DIR)
    clean_collection()
    fetch_repo(TARGET_REPO_URL, CLONE_DIR)
    ingest()
    print("Reindex completed successfully.")
    
if __name__ == "__main__":
    reindex()