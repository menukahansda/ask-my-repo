from langchain_core.tools import tool

from app.rag.retriever import retrieve


@tool
def search_codebase(query: str, repo_slug: str) -> str:
    """Semantic search over the repo's code and docs for relevant context."""
    embed_query_results = retrieve(query, repo_slug, 5)
    context_blocks = []
    for doc, meta in zip(embed_query_results["documents"][0], embed_query_results["metadatas"][0]):
        context_blocks.append(f"File: {meta['file_origin']}\n{doc}")

    context = "\n\n---\n\n".join(context_blocks)
    return context

