from .cmd import run


def run_black_format_check(repo_dir: str) -> bool:
    """
    Run Black in check mode to verify that the code is correctly formatted.

    :param repo_dir: The path to the repository directory. (e.g. /tmp/tmpdir1234)
    :return: True if the check passes, False otherwise
    """
    command = ["black", "--check", repo_dir]
    return run(command)
