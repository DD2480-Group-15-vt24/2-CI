import subprocess
from typing import (
    List,
    Tuple,
)  # Note: Python version 3.8.10 does not support subscript notation. Workaround: use List type from typing module


def run(command: List[str]) -> Tuple[bool, str]:
    """
    Run a command and return True if it succeeds, False otherwise.

    :param command: The command to run as a list of strings. (e.g. ["black", "--check", "."])
    :return: True if the command succeeds, False otherwise
    """
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logs = result.stdout + "\n" + result.stderr
        return True, logs
    except subprocess.CalledProcessError as e:
        logs = e.stdout + "\n" + e.stderr
        return False, logs
