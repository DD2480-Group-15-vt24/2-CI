import httpx
import os
from enum import Enum

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "no-token")


class State(Enum):
    """
    Types of commit status states
    """

    ERROR = "error"
    FAILURE = "failure"
    PENDING = "pending"
    SUCCESS = "success"


class CIType:
    """
    CI types
    """

    FORMAT = {
        "context": "FORMAT",
        "description": "Formatting pipeline result",
        # "target_url": "http://example.com/build/status",  # TODO: URL for more details (frontend)
    }
    TEST = {
        "context": "TEST",
        "description": "Test pipeline result",
    }


async def create_commit_status(
    owner: str, repo: str, sha: str, state: State, ci_type: CIType
) -> None:
    """
    Create a commit status for a given SHA

    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param sha: SHA for which the commit status is created
    :param state: The state of the status.
    :param ci_type: The CI type
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "state": state.value,
        **ci_type,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()  # This will raise an exception for 4XX/5XX responses
