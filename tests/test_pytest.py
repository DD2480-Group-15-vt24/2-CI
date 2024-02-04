import subprocess
import pytest
from unittest.mock import patch, MagicMock
from src.pytest import run_pytest_test_suite


@pytest.fixture
def mock_subprocess_run():
    """
    Mock the subprocess.run function to avoid running real commands
    """
    with patch("subprocess.run") as mock_run:
        yield mock_run


def test_run_black_success(mock_subprocess_run):
    """
    Test that clone_and_run_black returns True when Black check passes
    """

    # Mock subprocess.run to simulate Black check passing
    mock_subprocess_run.return_value = MagicMock(check_returncode=lambda: None)

    result = run_pytest_test_suite("/tmp/example123")

    assert result is True, "Expected pytest tests to pass"


def test_run_black_failure(mock_subprocess_run):
    """
    Test that clone_and_run_black returns False when Black check fails
    """
    # Mock subprocess.run to simulate Black check failing
    cmd = ["pytest", "."]
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, cmd=cmd)

    result = run_pytest_test_suite("/tmp/example123")

    assert result is False, "Expected pytest tests to fail"
