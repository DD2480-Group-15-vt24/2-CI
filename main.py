from fastapi import FastAPI, Request, HTTPException

from src.black import run_black_format_check
from src.git import clone_repo
from src.pytest import run_pytest_test_suite
from src.github import create_commit_status, State, CIType

app = FastAPI()


@app.post("/webhook/format/")
async def webhook_format(request: Request):
    payload = await request.json()
    sha = payload["head_commit"]["id"]
    owner = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]
    await create_commit_status(owner, repo, sha, State.PENDING, CIType.FORMAT)
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    if run_black_format_check(repo_dir):
        await create_commit_status(owner, repo, sha, State.SUCCESS, CIType.FORMAT)
        return {"status": "formatting check passed"}
    else:
        await create_commit_status(owner, repo, sha, State.FAILURE, CIType.FORMAT)
        raise HTTPException(status_code=422, detail="formatting check failed")


@app.post("/webhook/test/")
async def webhook_test(request: Request):
    payload = await request.json()
    sha = payload["head_commit"]["id"]
    owner = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]
    await create_commit_status(owner, repo, sha, State.PENDING, CIType.TEST)
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    if run_pytest_test_suite(repo_dir):
        await create_commit_status(owner, repo, sha, State.SUCCESS, CIType.TEST)
        return {"status": "tests passed"}
    else:
        await create_commit_status(owner, repo, sha, State.FAILURE, CIType.TEST)
        raise HTTPException(status_code=422, detail="tests failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8015)
