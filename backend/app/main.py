from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import CLONE_DIR, REINDEX_TOKEN
from app.ingest.fetch_repo import fetch_repo, clean_repo
from app.ingest.embed import ingest
from app.rag.chat import chat
from app.db.vectorstore import clean_collection

PORT = 8000


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    n_results: int = 5


@app.get("/")
def check_health():
    return JSONResponse(status_code=200, content={"message": "Service is healthy"})


@app.post("/ingest")
def ingest_repo(request: IngestRequest, x_reindex_token: str = Header(None)):
    if x_reindex_token != REINDEX_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = fetch_repo(request.repo_url)
    if not result["success"]:
        status_code = 400 if result["error"] == "invalid_url" else 502
        return JSONResponse(
            status_code=status_code, content={"message": result["message"]}
        )
        
    clean_collection()
    ingest(result["clone_dir"])
    return JSONResponse(status_code=200, content={"message": "Ingestion complete"})


@app.post("/chat")
def get_answer(request: ChatRequest):
    response = chat(request.question, request.n_results)
    return JSONResponse(status_code=200, content=response)


@app.post("/cleanup")
def cleanup():
    clean_repo(CLONE_DIR)
    return JSONResponse(status_code=200, content={"message": "Cleanup completed"})


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="127.0.0.1", port=PORT)
