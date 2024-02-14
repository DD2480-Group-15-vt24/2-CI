import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_clone_repo():
    with patch("main.clone_repo", return_value="/path/to/repo") as mock:
        yield mock


@pytest.fixture
def mock_github_status_response():
    with patch("main.create_commit_status", return_value=None) as mock:
        yield mock


@pytest.mark.parametrize(
    "endpoint, mock_function_path, mock_return, expected_status, expected_response",
    [
        (
            "/webhook/format/",
            "main.run_black_format_check",
            (True, ""),
            200,
            {"status": "formatting check passed"},
        ),
        (
            "/webhook/format/",
            "main.run_black_format_check",
            (False, ""),
            422,
            {"detail": "formatting check failed"},
        ),
        (
            "/webhook/test/",
            "main.run_pytest_test_suite",
            (True, ""),
            200,
            {"status": "tests passed"},
        ),
        (
            "/webhook/test/",
            "main.run_pytest_test_suite",
            (False, ""),
            422,
            {"detail": "tests failed"},
        ),
    ],
)
def test_webhook_actions(
    client,
    mock_clone_repo,
    endpoint,
    mock_function_path,
    mock_github_status_response,
    mock_return,
    expected_status,
    expected_response,
):
    with patch(mock_function_path, return_value=mock_return) as _mock_function:
        response = client.post(
            endpoint,
            json={
                "repository": {
                    "name": "myname",
                    "clone_url": "https://github.com/example/repo.git",
                    "owner": {
                        "login": "mock_owner",
                    },
                },
                "ref": "refs/heads/main",
                "head_commit": {
                    "id": "1234",
                    "message": "test commit",
                },
            },
        )
        assert response.status_code == expected_status
        assert response.json() == expected_response
