import os
import shutil
import stat

from git import Repo

from app.config import TARGET_REPO_URL, CLONE_DIR


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
    pass