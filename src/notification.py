import requests
from enum import Enum


class State(Enum):
    ERROR = "error"
    FAILURE = "failure"
    PENDING = "pending"
    SUCCESS = "success"


def create_commit_status(
    owner: str, repo: str, sha: str, state: State, token: str
) -> bool:
    """
    Create a commit status for a given SHA.

    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param sha: SHA for which the commit status is created
    :param state: The state of the status.
    :param target_url: The target URL to associate with this tatus.
    :param token: Token for authenticating to the GitHub REST API
    :return: True if commit status was successfully created, False otherwise
    """

    endpoint = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }

    payload = {"state": state.name}

    response = requests.post(endpoint, headers=headers, json=payload)

    return response.status_code == 201
