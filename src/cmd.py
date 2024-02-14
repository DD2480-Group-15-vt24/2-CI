import subprocess
from typing import (
    List,
)  # Note: Python version 3.8.10 does not support subscript notation. Workaround: use List type from typing module


def run(command: List[str]) -> bool:
    """
    Run a command and return True if it succeeds, False otherwise.

    :param command: The command to run as a list of strings. (e.g. ["black", "--check", "."])
    :return: True if the command succeeds, False otherwise
    """
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False
