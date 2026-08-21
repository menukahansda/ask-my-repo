import os
import shutil
import stat
import time
from pathlib import Path
from urllib.parse import urlparse

from git import Repo
from git.exc import GitCommandError

from app.config import CLONE_DIR, TARGET_REPO_URL
from app.logging_config import get_logger

logger = get_logger(__name__)
STALE_DAYS = 3

def validate_url(target_repo_url):
    """Validates a GitHub repo URL. Returns dict on success, None otherwise."""
    if not target_repo_url:
        return None

    target_repo_url = target_repo_url.strip()

    parsed = urlparse(target_repo_url)

    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.netloc.lower() != "github.com":
        return None

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None

    owner, repo = parts[0], parts[1]
    repo = repo.removesuffix(".git")

    if not owner or not repo:
        return None

    repo_slug = f"{owner}-{repo}"
    normalized_url = f"https://github.com/{owner}/{repo}.git"

    return {"target_repo_url": normalized_url, "repo_slug": repo_slug}


def fetch_repo(target_repo_url):
    result = validate_url(target_repo_url)
    if result is None:
        return {
            "success": False,
            "error": "invalid_url",
            "message": "The provided URL is not a valid GitHub repository URL.",
        }

    os.makedirs(CLONE_DIR, exist_ok=True)
    clone_dir_path = Path(CLONE_DIR) / result["repo_slug"]

    if (clone_dir_path / ".git").exists():
        logger.info(f"reusing existing clone at {clone_dir_path} — will NOT re-ingest")
        return {
            "success": True,
            "already_cloned": True,
            "message": "Cloned repo already exists",
            "clone_dir": str(clone_dir_path),
            "repo_slug": result["repo_slug"],
        }
    try:
        Repo.clone_from(result["target_repo_url"], clone_dir_path)
    except GitCommandError as e:
        logger.error(f"clone failed for {target_repo_url}: {e}")
        return {
            "success": False,
            "error": "clone_failed",
            "message": "Could not clone the repository. It may be private, not exist, or there was a network issue.",
        }

    return {
        "success": True,
        "already_cloned": False,
        "message": "Cloning completed.",
        "clone_dir": str(clone_dir_path),
        "repo_slug": result["repo_slug"],
    }


def clean_repo(clone_dir):
    def remove_readonly(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onexc=remove_readonly)
        print("Repository cleaned up.")

def cleanup_stale_repos():
    cutoff = time.time() - STALE_DAYS * 86400
    clone_path = Path(CLONE_DIR)
    if not clone_path.exists():
        return

    from app.db.vectorstore import (
        clean_collection,  # local import avoids a circular import risk
    )

    for repo_dir in clone_path.iterdir():
        if repo_dir.is_dir() and repo_dir.stat().st_mtime < cutoff:
            logger.info(f"Cleaning up stale repo: {repo_dir.name}")
            clean_collection(repo_dir.name)
            clean_repo(str(repo_dir))
            
if __name__ == "__main__":
    result = fetch_repo(TARGET_REPO_URL)
    print("Result:\n", result)
    # clean_repo(CLONE_DIR)
