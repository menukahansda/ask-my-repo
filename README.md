# ask-my-repo
A RAG chatbot over a GitHub repo's code/docs, with a CI/CD pipeline that checks daily and reindexes the vector store when the target repo has changed.

Live demo: [ask-my-repo-steel.vercel.app](https://ask-my-repo-steel.vercel.app/)

> Note: the backend is hosted on Render's free tier, which spins down after inactivity — the first request after idle time may take up to a minute to respond.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Running the App](#running-the-app)
- [Known Limitations](#known-limitations)

---

## Project Structure

```
ask-my-repo/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint
│   │   ├── config.py            # env vars, API keys
│   │   ├── logging_config.py    # logging setup
│   │   ├── agent/               # LangChain agent — local branch only, not on main, not wired into /chat yet
│   │   │   ├── graph.py
│   │   │   ├── state.py
│   │   │   └── tools.py
│   │   ├── ingest/
│   │   │   ├── fetch_repo.py    # clone/pull target repo
│   │   │   ├── chunker.py       # split code/docs into chunks
│   │   │   └── embed.py         # call embedding API, upsert to vector DB
│   │   ├── rag/
│   │   │   ├── retriever.py     # similarity search over vector DB
│   │   │   └── chat.py          # prompt template + LLM call + citation formatting
│   │   └──  db/
│   │       └── vectorstore.py   # ChromaDB client wrapper
│   │ 
│   ├── dev_scripts/
│   │   └── test_query.py        # test if retriever and embed works 
│   ├── scripts/
│   │   └── reindex_cli.py       # manual trigger for the same reindex logic
│   ├── tests/                   # pytest suite run by CI (ci.yml)
│   │   ├── test_chunker.py
│   │   ├── test_fetch_repo.py
│   │   └── test_vectorstore.py
│   ├── agent_tester.py          # standalone script for exercising the agent — local branch only
│   ├── pytest.ini
│   ├── requirements.txt
│   └── Dockerfile      
│          
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── ChatScreen.tsx
│   │   │   └── RepoOnboarding.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       ├── ci.yml               # lint/test on push
│       └── reindex.yml          # triggered reindex job
├── package.json                 # root "npm run dev" — runs backend + frontend together
└── README.md
```

---

## Features
- Clone and ingest any public GitHub repository
- Automatic chunking of code and documentation files
- Semantic search over repo content using Gemini embeddings + ChromaDB
- Natural-language Q&A powered by Gemini, with self-reported source citations
- REST API (FastAPI) + web UI (Next.js)
- CI/CD pipeline (GitHub Actions) for linting, testing, and vector store reindexing

---

## How It Works

1. **User pastes a GitHub repo URL** → frontend sends it to `POST /ingest`
2. **Backend clones the repo**, walks its files, splits them into chunks, generates embeddings via Gemini, and stores them in ChromaDB
3. **User asks a question** → frontend sends it to `POST /chat`
4. **Backend embeds the question**, retrieves the most relevant chunks from ChromaDB via similarity search, and passes them as context to Gemini
5. **Gemini generates an answer** grounded in the retrieved code/docs, along with the specific files it used
6. **User receives the answer and cited source files** in the chat UI

---

## Tech Stack

**Backend**: FastAPI, ChromaDB, Google Gemini (embeddings + chat), GitPython
**Frontend**: Next.js, React
**CI/CD**: GitHub Actions

---

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```
Create a `.env` file in `backend/`:
```
GEMINI_API_KEY=your-key-here
```

### Frontend
```bash
cd frontend
npm install
```
Create `.env.local` in `frontend/`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Running the App

### Both (from repo root)
```bash
npm install
npm run dev
```
Runs backend + frontend together via `concurrently`.

> ⚠️ Currently Windows-only (the script hardcodes `venv\Scripts\python`). On macOS/Linux, run backend and frontend separately using the sections below.

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```
API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm run dev
```
App available at `http://localhost:3000`.

---

## Known Limitations
- Public repositories only (no authentication for private repos)
- Citations reflect the model's self-reported sources from retrieved context, not strict per-line verification
- Uses Gemini's free-tier API, which enforces a 100 requests/minute quota on embeddings. Ingesting multiple repos in quick succession may hit this limit; space out /ingest calls by ~20-30s if you see repeated failures.

