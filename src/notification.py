import requests
import os
from enum import Enum


class State(Enum):
    ERROR = "error"
    FAILURE = "failure"
    PENDING = "pending"
    SUCCESS = "success"


def create_commit_status(owner: str, repo: str, sha: str, state: State) -> bool:
    """
    Create a commit status for a given SHA.

    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param sha: SHA for which the commit status is created
    :param state: The state of the status.
    :return: True if commit status was successfully created, False otherwise
    """

    endpoint = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"

    token = read_token_from_file("src/token.txt")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }

    payload = {"state": state.name}

    response = requests.post(endpoint, headers=headers, json=payload)

    return response.status_code == 201


def read_token_from_file(filepath: str) -> str:
    """
    Read one line from a file.

    :param filepath: Path to file
    :return: The first line of the specified file
    """
    if os.path.exists(filepath):
        file = open(filepath)
        token = file.readline()
        file.close()
        return token
    else:
        raise Exception(
            "No API token provided. Please create src/token.txt and provide the GitHub API token."
        )
