import pytest


@pytest.fixture
def fake_repo(tmp_path):
    """A tmp_path pre-populated with a small fake repo tree, for chunker tests."""
    (tmp_path / "sub" / "folder").mkdir(parents=True)
    (tmp_path / "small.py").write_text("x = 1")
    (tmp_path / "big.py").write_text("a" * 2500)
    (tmp_path / "sub" / "folder" / "file.py").write_text("x = 1")
    return tmp_path