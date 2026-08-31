import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLONE_DIR = "./cloned_repos"
TARGET_REPO_URL = "https://github.com/menukahansda/task-management-system.git"
