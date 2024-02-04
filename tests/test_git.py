import os
from src.git import clone_repo
from unittest.mock import patch
import pytest


@pytest.fixture
def mock_repo_clone_from():
    """
    Mock the git.Repo.clone_from method to avoid cloning a real repository
    """
    with patch("git.Repo.clone_from") as mock_clone:
        yield mock_clone


def test_clone_repo(mock_repo_clone_from):
    """
    Test that clone_repo returns the path to the cloned repository
    """
    # Mock the clone_from method to avoid cloning a real repository
    mock_repo_clone_from.return_value = None

    result = clone_repo("https://github.com/example/repo.git", "main")

    # assert that the result is a directory
    assert os.path.isdir(result), "Expected a directory path"
