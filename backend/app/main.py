from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import CLONE_DIR
from app.ingest.fetch_repo import fetch_repo, clean_repo
from app.ingest.embed import ingest
from app.rag.chat import chat
from app.db.vectorstore import collection

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
    return {"health": "good"}


@app.post("/ingest")
def ingest_repo(request: IngestRequest):
    clean_repo(CLONE_DIR)   
         
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        
    fetch_repo(request.repo_url, CLONE_DIR)
    ingest()
    return {"status": "ingestion complete"}

@app.post("/chat")
def get_answer(request: ChatRequest):
    response = chat(request.question, request.n_results)
    return response


@app.post("/cleanup")
def cleanup():
    clean_repo(CLONE_DIR)
    return {"cleanup": "Completed"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="127.0.0.1", port=PORT)
