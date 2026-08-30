from pathlib import Path

from git import Repo
from langchain_core.tools import tool

from app.config import CLONE_DIR
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

@tool
def read_file(file_path: str, repo_slug: str) -> str:
    """Read the full contents of a specific file in the cloned repo."""
    # TODO: resolve file_path against cloned_repos/{repo_slug}/, read it
    # think about: what happens if the path doesn't exist, or escapes the repo dir?
    root = (Path(CLONE_DIR) / repo_slug).resolve()
    target = (root / file_path).resolve()
    
    if not target.is_relative_to(root):
        raise ValueError("Path is outside repository.")
    
    if not target.is_file():
        raise ValueError("File not found or path is not to any file.")
    
    content = target.read_text(encoding="utf-8", errors="ignore")
    return content
    
@tool
def git_blame(file_path: str, repo_slug: str) -> str:
    """Show line-by-line commit history for a file."""
    root = (Path(CLONE_DIR) / repo_slug).resolve()
    target = (root / file_path).resolve()

    if not target.is_relative_to(root):
        raise ValueError("Path is outside repository.")

    if not target.is_file():
        raise ValueError("File not found or path is not to any file.")

    repo = Repo(root)

    result = repo.blame("HEAD", file_path)

    content = []
    start_line = 1

    for commit, lines in result:
        end_line = start_line + len(lines) - 1

        content.append(
            f"Lines {start_line}-{end_line}\n"
            f"Commit: {commit.hexsha}\n"
            f"Author: {commit.author}\n"
            f"Date: {commit.committed_datetime}\n"
            f"Message: {commit.message.strip()}"
        )

        start_line = end_line + 1

    return "\n\n---\n\n".join(content)