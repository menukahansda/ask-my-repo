import pytest
from app.ingest.chunker import chunk_file


class TestChunkFile:
    def test_chunks_short_file(self, fake_repo):
        f = fake_repo / "small.py"
        chunks = chunk_file(fake_repo, f, chunk_size=1000, overlap=100)
        assert len(chunks) == 1
        assert chunks[0]["content"] == "x = 1"
        assert chunks[0]["metadata"]["file_origin"] == "small.py"
        assert chunks[0]["metadata"]["chunk_index"] == 0

    def test_chunks_long_file_into_multiple_pieces(self, fake_repo):
        f = fake_repo / "big.py"
        chunks = chunk_file(fake_repo, f, chunk_size=1000, overlap=100)
        assert len(chunks) > 1
        # consecutive chunks should overlap by `overlap` chars
        assert chunks[0]["content"][-100:] == chunks[1]["content"][:100]

    def test_chunk_ids_are_unique(self, fake_repo):
        f = fake_repo / "big.py"
        chunks = chunk_file(fake_repo, f, chunk_size=1000, overlap=100)
        ids = [c["id"] for c in chunks]
        assert len(ids) == len(set(ids))

    def test_no_chunk_has_empty_content(self, fake_repo):
        f = fake_repo / "small.py"
        chunks = chunk_file(fake_repo, f)
        assert all(c["content"].strip() for c in chunks)

    def test_relative_path_uses_forward_slashes(self, fake_repo):
        f = fake_repo / "sub" / "folder" / "file.py"
        chunks = chunk_file(fake_repo, f)
        assert chunks[0]["metadata"]["file_origin"] == "sub/folder/file.py"

    def test_overlap_must_be_smaller_than_chunk_size(self, fake_repo):
        f = fake_repo / "small.py"
        with pytest.raises(AssertionError):
            chunk_file(fake_repo, f, chunk_size=100, overlap=100)