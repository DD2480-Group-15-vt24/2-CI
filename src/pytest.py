from .cmd import run


def run_pytest_test_suite(repo_dir: str) -> bool:
    """
    Run pytest in the repository directory to execute the tests.

    :param repo_dir: The path to the repository directory. (e.g. /tmp/tmpdir1234)
    :return: True if the check passes, False otherwise
    """

    command = ["pytest", repo_dir]
    return run(command)
