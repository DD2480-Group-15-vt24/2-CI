import tempfile

from git import Repo


def clone_repo(repo_url: str, branch: str) -> str:
    """
    Clones the repository to a temporary directory and returns the directory path.
    """
    tmpdirname = tempfile.mkdtemp()
    Repo.clone_from(repo_url, tmpdirname, branch=branch)
    return tmpdirname
