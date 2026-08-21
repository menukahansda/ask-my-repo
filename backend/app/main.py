from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.db.vectorstore import clean_collection
from app.ingest.embed import ingest
from app.ingest.fetch_repo import cleanup_stale_repos, fetch_repo
from app.rag.chat import chat

PORT = 8000


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_stale_repos()
    print("Model loaded and ready.")
    yield
    print("Shutting down.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class IngestRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    question: str
    repo_slug: str
    n_results: int = 5


@app.get("/")
def check_health():
    return JSONResponse(status_code=200, content={"message": "Service is healthy"})


@app.post("/ingest")
def ingest_repo(request: IngestRequest):

    result = fetch_repo(request.repo_url)
    if not result["success"]:
        status_code = 400 if result["error"] == "invalid_url" else 502
        return JSONResponse(
            status_code=status_code, content={"message": result["message"]}
        )

    if not result["already_cloned"]:
        clean_collection(result["repo_slug"])
        ingest(result["clone_dir"], result["repo_slug"])
    return JSONResponse(
        status_code=200,
        content={
            "message": "Ingestion complete",
            "repo_slug": result["repo_slug"],
        },
    )


@app.post("/chat")
def get_answer(request: ChatRequest):
    response = chat(request.question, request.repo_slug, request.n_results)
    return JSONResponse(status_code=200, content=response)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", reload=True, reload_dirs=["app"], host="127.0.0.1", port=PORT
    )
