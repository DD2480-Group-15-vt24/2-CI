from fastapi import FastAPI, Request, HTTPException

from src.black import run_black_format_check
from src.git import clone_repo
from src.pytest import run_pytest_test_suite
from db import insert_row
app = FastAPI()


@app.post("/webhook/format/")
async def webhook_format(request: Request):
    payload = await request.json()
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    if run_black_format_check(repo_dir):
        return {"status": "formatting check passed"}
    else:
        raise HTTPException(status_code=422, detail="formatting check failed")


@app.post("/webhook/test/")
async def webhook_test(request: Request):
    payload = await request.json()
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    success,logs = run_pytest_test_suite(repo_dir)
    insert_row(repo_url, logs)

    # here I have to add rows to the data base and db we --

    if success:
        return {"status": "tests passed"}
    else:
        raise HTTPException(status_code=422, detail="tests failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
