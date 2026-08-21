import sys

from app.db.vectorstore import clean_collection
from app.ingest.embed import ingest
from app.ingest.fetch_repo import fetch_repo
from app.rag.retriever import retrieve

repo_url = "https://github.com/menukahansda/task-management-system"

result = fetch_repo(repo_url)
if not result["success"]:
    print(f"fetch_repo failed: {result['message']}")
    sys.exit(1)

if not result["already_cloned"]:
    clean_collection(result["repo_slug"])
    ingest(result["clone_dir"], result["repo_slug"])

repo_slug = result["repo_slug"]

results = retrieve(
    "What is the workflow of this project?",
    repo_slug,
)

print(results)
