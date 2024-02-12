import pytest
from unittest.mock import patch, MagicMock
from src.notification import create_commit_status, State, read_token_from_file


@pytest.fixture
def token_file(tmp_path):
    """
    Mock a token file
    """
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    token_file = src_dir / "token.txt"
    token_file.write_text("token")
    return token_file


def read_token_from_file_success(token_file):
    """
    Test reading a file that exists
    """
    token = read_token_from_file(token_file)
    assert token == "token"


def read_token_from_file_failure(tmp_path):
    """
    Test reading a file that does not exists
    """
    with pytest.raises(Exception):
        read_token_from_file(tmp_path / "random.txt")


@pytest.mark.parametrize(
    "status_code, expected_result",
    [
        (201, True),
        (404, False),
    ],
)
@patch("requests.post")
def test_create_commit_status(mock_post, status_code, expected_result):
    """
    Test that API requests to create commit statuses are correctly formated.
    Also, test that when receiving an API response, the function returns correctly based on response status code.
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_post.return_value = mock_response

    owner = "owner"
    repo = "repo"
    sha = "1234"
    state = State.SUCCESS
    token = "token"

    result = create_commit_status(owner, repo, sha, state)

    assert result == expected_result

    mock_post.assert_called_once_with(
        f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        },
        json={"state": state.name},
    )
