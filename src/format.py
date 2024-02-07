import subprocess
import tempfile
from git import Repo


def clone_and_run_black(repo_url: str, branch: str) -> bool:
    """
    Clone the repository at the specified URL and run Black in check mode.

    :param repo_url: The URL of the repository to clone
    :param branch: The branch to clone
    :return: True if Black check passes, False otherwise
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(repo_url, tmpdirname, branch=branch)
        black_command = ["black", "--check", tmpdirname]
        try:
            subprocess.run(black_command, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError:
            return False
