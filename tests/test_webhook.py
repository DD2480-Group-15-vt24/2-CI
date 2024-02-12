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


@pytest.mark.parametrize(
    "endpoint, mock_function_path, mock_return, expected_status, expected_response",
    [
        (
            "/webhook/format/",
            "main.run_black_format_check",
            True,
            200,
            {"status": "formatting check passed"},
        ),
        (
            "/webhook/format/",
            "main.run_black_format_check",
            False,
            422,
            {"detail": "formatting check failed"},
        ),
        (
            "/webhook/test/",
            "main.run_pytest_test_suite",
            True,
            200,
            {"status": "tests passed"},
        ),
        (
            "/webhook/test/",
            "main.run_pytest_test_suite",
            False,
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
    mock_return,
    expected_status,
    expected_response,
    tmp_path,
):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    token_file = src_dir / "token.txt"
    token_file.write_text("token")
    with patch(mock_function_path, return_value=mock_return) as _mock_function:
        response = client.post(
            endpoint,
            json={
                "repository": {"clone_url": "https://github.com/example/repo.git"},
                "ref": "refs/heads/main",
                "head_commit": {"id": "1234"},
            },
        )
        assert response.status_code == expected_status
        assert response.json() == expected_response
