import os
import shutil
import stat

from git import Repo
from urllib.parse import urlparse

from app.config import TARGET_REPO_URL, CLONE_DIR


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
    if repo.endswith(".git"):
        repo = repo[:-4]

    if not owner or not repo:
        return None

    clone_subdir = f"{owner}-{repo}"
    normalized_url = f"https://github.com/{owner}/{repo}.git"

    return {"target_repo_url": normalized_url, "clone_subdir": clone_subdir}


def fetch_repo(target_repo_url, clone_dir):
    Repo.clone_from(target_repo_url, clone_dir)
    print("Cloning completed.")


def clean_repo(clone_dir):
    def remove_readonly(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onexc=remove_readonly)
        print("Repository cleaned up.")


if __name__ == "__main__":
    fetch_repo(TARGET_REPO_URL, CLONE_DIR)
    # clean_repo(CLONE_DIR)
