import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLONE_DIR = "./cloned_repos"
TARGET_REPO_URL = "https://github.com/menukahansda/task-management-system.git"
