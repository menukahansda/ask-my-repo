from app.rag.retriever import retrieve

results = retrieve("What is the workflow of this project?")

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(meta["file_origin"], "-", doc[:100])