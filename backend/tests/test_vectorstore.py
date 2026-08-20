from app.db.vectorstore import _sanitize_name


class TestSanitizeName:
    def test_valid_repo_slug_passthrough(self):
        assert _sanitize_name("menukahansda-task-management-system") == (
            "menukahansda-task-management-system"
        )

    def test_replaces_invalid_chars(self):
        assert _sanitize_name("menukahansda/task-management-system@v2") == (
            "menukahansda-task-management-system-v2"
        )

    def test_strips_leading_trailing_separators(self):
        assert (
            _sanitize_name(
                "-menukahansda-task-management-system-"
            )
            == "menukahansda-task-management-system"
        )

    def test_truncates_to_63_chars(self):
        long_slug = "a" * 100

        sanitized_name = _sanitize_name(long_slug)

        assert len(sanitized_name) <= 63

    def test_empty_input_falls_back_to_repo(self):
        assert _sanitize_name("") == "repo"

    def test_same_slug_produces_same_name(self):
        # Same repo slug must always map to the same collection name.
        slug = "menukahansda-task-management-system"

        assert _sanitize_name(slug) == _sanitize_name(slug)