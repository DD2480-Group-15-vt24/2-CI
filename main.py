from fastapi import FastAPI, Request, HTTPException

from src.format import clone_and_run_black

app = FastAPI()


@app.post("/webhook/")
async def webhook(request: Request):
    # Parse the request body as JSON
    payload = await request.json()
    repo_url = payload["repository"]["clone_url"]
    # GitHub webhook sends full ref in the format "refs/heads/branch_name"
    branch = payload["ref"].split("/")[-1]

    # Clone the repo and run Black
    check_passed = clone_and_run_black(repo_url, branch)
    if check_passed:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=422, detail="Formatting check failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
