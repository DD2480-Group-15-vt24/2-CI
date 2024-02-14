import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx  # Make sure to import httpx
from src.github import create_commit_status, State, CIType


@pytest.mark.asyncio
async def test_create_commit_status_success(mocker):
    # Mock the AsyncClient.post method to return a successful response
    mock_post = AsyncMock()
    mocker.patch("httpx.AsyncClient.post", new=mock_post)

    # Call the function with test data
    await create_commit_status(
        "test_owner", "test_repo", "test_sha", State.SUCCESS, CIType.FORMAT
    )

    # Assert the post method was called with the expected arguments
    mock_post.assert_awaited_once()

    # Extract the actual call arguments
    actual_args, actual_kwargs = mock_post.call_args

    # Corrected assertions
    expected_url = "https://api.github.com/repos/test_owner/test_repo/statuses/test_sha"
    assert actual_args[0] == expected_url  # The URL is the first positional argument
    assert actual_kwargs["json"]["state"] == "success"
    assert actual_kwargs["json"]["context"] == "FORMAT"


@pytest.mark.asyncio
async def test_create_commit_status_unauthorized(mocker):
    # Prepare the exception to be raised by the mock
    mock_exception = httpx.HTTPStatusError(
        message="Unauthorized", request=MagicMock(), response=MagicMock()
    )

    # Mock the AsyncClient.post method to raise HTTPStatusError
    mock_post = mocker.patch("httpx.AsyncClient.post", side_effect=mock_exception)

    # Expect the function to raise an HTTPStatusError due to unauthorized access
    with pytest.raises(httpx.HTTPStatusError):
        await create_commit_status(
            "test_owner", "test_repo", "test_sha", State.ERROR, CIType.TEST
        )

    mock_post.assert_awaited_once()
