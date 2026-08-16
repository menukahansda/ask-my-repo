# walk into files

# chunk them, print and count

import os
from pathlib import Path

from app.config import CLONE_DIR

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "dist",
    "build",
    ".next",
    "coverage",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".log",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
}

EXCLUDE_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    ".gitignore",
}

CHUNK_SIZE = 1000
OVERLAP = 100


def chunk_file(clone_dir, file_path, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Read one file and return its chunks."""

    assert overlap < chunk_size, "overlap must be smaller than chunk_size"
    relative_path = file_path.relative_to(clone_dir).as_posix()

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk = {
            "id": f"{relative_path}::chunk_{chunk_index}",
            "content": text[start:end],
            "metadata": {
                "file_origin": relative_path,
                "chunk_index": chunk_index,
            },
        }

        chunks.append(chunk)

        chunk_index += 1
        start += chunk_size - overlap

    return chunks


def walk_and_chunk_files(clone_dir):
    clone_dir = Path(clone_dir)

    if not clone_dir.exists():
        print(f"Directory {clone_dir} does not exist.")
        return

    output_file = "chunks.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("CHUNK PREVIEW\n")
        f.write("=" * 80 + "\n\n")

    total_files = 0
    total_chunks = 0
    all_chunks = []

    for dirpath, dirnames, filenames in os.walk(clone_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if (
                Path(filename).suffix.lower() in EXCLUDE_EXTS
                or filename.startswith(".")
                or filename in EXCLUDE_FILES
            ):
                continue

            file_path = Path(dirpath) / filename

            try:
                chunks = chunk_file(clone_dir, file_path)
            except (OSError, UnicodeDecodeError) as e:
                print(f"Skipping {file_path}: {e}")
                continue

            total_files += 1
            with open(output_file, "a", encoding="utf-8") as f:
                for chunk in chunks:
                    f.write("=" * 80 + "\n")
                    f.write(f"FILE: {chunk['metadata']['file_origin']}\n")
                    f.write(f"CHUNK: {chunk['metadata']['chunk_index']}\n")
                    f.write(f"ID: {chunk['id']}\n")
                    f.write("=" * 80 + "\n")
                    f.write(chunk["content"])
                    f.write("\n\n")
                    total_chunks += 1
                    all_chunks.append(chunk)

    print(f"Files processed: {total_files}")
    print(f"Chunks created: {total_chunks}")
    print(f"Preview saved to: {output_file}")

    return all_chunks


if __name__ == "__main__":
    walk_and_chunk_files(CLONE_DIR)
