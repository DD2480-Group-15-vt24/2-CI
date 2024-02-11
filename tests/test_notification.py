import pytest
from unittest.mock import patch, MagicMock
from src.notification import create_commit_status, State


@pytest.mark.parametrize(
    "status_code, expected_result",
    [
        (201, True),
        (404, False),
    ],
)
@patch("requests.post")
def test_create_commit_status(mock_post, status_code, expected_result):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_post.return_value = mock_response

    owner = "owner"
    repo = "repo"
    sha = "1234"
    state = State.SUCCESS
    token = "token"

    result = create_commit_status(owner, repo, sha, state, token)

    assert result == expected_result

    mock_post.assert_called_once_with(
        f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        },
        json={"state": state.name},
    )
