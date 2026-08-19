from app.rag.retriever import retrieve

repo_slug = "menukahansda-task-management-system"

results = retrieve(
    "What is the workflow of this project?",
    repo_slug,
)

print(results)
