from app.ingest.fetch_repo import validate_url

EXPECTED = {
    "target_repo_url": "https://github.com/menukahansda/task-management-system.git",
    "repo_slug": "menukahansda-task-management-system",
}


def test_extra_path_segments():
    assert (
        validate_url(
            "https://github.com/menukahansda/task-management-system/commits/main/"
        )
        == EXPECTED
    )


def test_owner_only_trailing_slash():
    assert validate_url("https://github.com/menukahansda/") is None


def test_clean_url():
    assert (
        validate_url("https://github.com/menukahansda/task-management-system")
        == EXPECTED
    )


def test_valid_url_with_query_and_fragment():
    assert (
        validate_url(
            "https://github.com/menukahansda/task-management-system"
            "?tab=readme#section"
        )
        == EXPECTED
    )


def test_root_only():
    assert validate_url("https://github.com/") is None


def test_non_github_domain():
    assert (
        validate_url(
            "https://www.youtube.com/watch?v=EbI74XqaJ_0" "&list=RD9aED02XuLwo&index=2"
        )
        is None
    )


def test_owner_only_with_query_string():
    assert validate_url("https://github.com/menukahansda?tab=repositories") is None


def test_empty_string():
    assert validate_url("") is None


def test_none_input():
    assert validate_url(None) is None


def test_whitespace_padding():
    assert (
        validate_url("  https://github.com/menukahansda/task-management-system  ")
        == EXPECTED
    )


def test_already_has_git_suffix():
    assert (
        validate_url("https://github.com/menukahansda/task-management-system.git")
        == EXPECTED
    )


def test_uppercase_domain():
    assert (
        validate_url("https://GITHUB.COM/menukahansda/task-management-system")
        == EXPECTED
    )


def test_ssh_style_url_rejected():
    assert (
        validate_url("git@github.com:menukahansda/task-management-system.git") is None
    )


def test_gist_subdomain_rejected():
    assert validate_url("https://gist.github.com/menukahansda/somehash") is None


def test_double_slash_in_path():
    assert (
        validate_url("https://github.com/menukahansda//task-management-system")
        == EXPECTED
    )


def test_http_scheme_accepted():
    assert (
        validate_url("http://github.com/menukahansda/task-management-system")
        == EXPECTED
    )
