import subprocess
import pytest
from unittest.mock import patch, MagicMock
from main import clone_and_run_black


@pytest.fixture
def mock_subprocess_run():
    """
    Mock the subprocess.run function to avoid running real commands
    """
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_repo_clone_from():
    """
    Mock the git.Repo.clone_from method to avoid cloning a real repository
    """
    with patch("git.Repo.clone_from") as mock_clone:
        yield mock_clone


def test_clone_and_run_black_success(mock_subprocess_run, mock_repo_clone_from):
    """
    Test that clone_and_run_black returns True when Black check passes
    """

    # Mock subprocess.run to simulate Black check passing
    mock_subprocess_run.return_value = MagicMock(check_returncode=lambda: None)

    result = clone_and_run_black("https://github.com/example/repo.git", "main")

    assert result is True, "Expected Black check to pass"


def test_clone_and_run_black_failure(mock_subprocess_run, mock_repo_clone_from):
    """
    Test that clone_and_run_black returns False when Black check fails
    """
    # Mock subprocess.run to simulate Black check failing
    cmd = ["black", "--check", "."]
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, cmd=cmd)

    result = clone_and_run_black("https://github.com/example/repo.git", "main")

    assert result is False, "Expected Black check to fail"
