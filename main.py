from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import desc


from src.black import run_black_format_check
from src.git import clone_repo
from src.pytest import run_pytest_test_suite
from src.github import create_commit_status, State, CIType
from src.db import database, webhook_events, insert_webhook_event


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/webhook/format/")
async def webhook_format(request: Request):
    payload = await request.json()
    sha = payload["head_commit"]["id"]
    commit_message = payload["head_commit"]["message"]
    owner = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]
    await create_commit_status(owner, repo, sha, State.PENDING, CIType.FORMAT)
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    success, logs = run_black_format_check(repo_dir)
    await insert_webhook_event(
        sha, commit_message, datetime.utcnow(), logs, success, "format"
    )
    if success:
        await create_commit_status(owner, repo, sha, State.SUCCESS, CIType.FORMAT)
        return {"status": "formatting check passed"}

    else:
        await create_commit_status(owner, repo, sha, State.FAILURE, CIType.FORMAT)
        raise HTTPException(status_code=422, detail="formatting check failed")


@app.post("/webhook/test/")
async def webhook_test(request: Request):
    payload = await request.json()
    sha = payload["head_commit"]["id"]
    commit_message = payload["head_commit"]["message"]
    owner = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]
    await create_commit_status(owner, repo, sha, State.PENDING, CIType.TEST)
    repo_url = payload["repository"]["clone_url"]
    branch = payload["ref"].split("/")[-1]
    repo_dir = clone_repo(repo_url, branch)
    success, logs = run_pytest_test_suite(repo_dir)
    await insert_webhook_event(
        sha, commit_message, datetime.utcnow(), logs, success, "test"
    )
    if success:
        await create_commit_status(owner, repo, sha, State.SUCCESS, CIType.TEST)
        return {"status": "tests passed"}
    else:
        await create_commit_status(owner, repo, sha, State.FAILURE, CIType.TEST)
        raise HTTPException(status_code=422, detail="tests failed")


@app.get("/events")
async def get_events():
    query = webhook_events.select().order_by(desc("datetime"))
    return await database.fetch_all(query)


@app.get("/events/{commit_hash}")
async def get_event(commit_hash: str):
    query = webhook_events.select().where(webhook_events.c.commit_hash == commit_hash)
    return await database.fetch_one(query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8015)
