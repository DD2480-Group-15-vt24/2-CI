from fastapi import FastAPI, Request, HTTPException

from src.black import run_black_format_check
from src.git import clone_repo
from src.pytest import run_pytest_test_suite
from src.notification import create_commit_status, State

# Repository settings
owner = "DD2480-Group-15-vt24"
repo = "2-CI"
token = "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"


app = FastAPI()


@app.post("/webhook/format/")
async def webhook_format(request: Request):
    payload = await request.json()
    sha = payload["head_commit"]["id"]
    create_commit_status(owner, repo, sha, State.PENDING, token)
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    if run_black_format_check(repo_dir):
        create_commit_status(owner, repo, sha, State.SUCCESS, token)
        return {"status": "formatting check passed"}
    else:
        create_commit_status(owner, repo, sha, State.FAILURE, token)
        raise HTTPException(status_code=422, detail="formatting check failed")


@app.post("/webhook/test/")
async def webhook_test(request: Request):
    payload = await request.json()
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    if run_pytest_test_suite(repo_dir):
        return {"status": "tests passed"}
    else:
        raise HTTPException(status_code=422, detail="tests failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
