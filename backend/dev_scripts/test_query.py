from app.rag.retriever import retrieve

results = retrieve("how does user login work")

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(meta["file_origin"], "-", doc[:100])