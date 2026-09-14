# Lenny OS — The Lenny Growth Assistant

Turn product wisdom into your next move. A full-stack AI conversational application grounded in Lenny's Podcast transcripts.

## Features
- **Real RAG Pipeline:** Uses pgvector to semantically search real podcast transcripts.
- **Strict Grounding:** The LLM is strictly instructed to only use retrieved evidence and cite its sources.
- **Evidence UI:** Every response visually displays the transcript chunks used to generate it.
- **Provider Abstraction:** Switch seamlessly between local (Ollama) and cloud (Anthropic) LLMs.
- **Agent Skills:** Generates Ship 30 essays, HTML/CSS artifacts, and structured Growth Plans.
- **Artifact Viewer:** Renders markdown and sandboxed HTML safely alongside the chat.
- **Premium Design:** Editorial typography (Newsreader/Inter) and a sophisticated warm color palette.

## Architecture & Tech Stack
- **Backend:** FastAPI, Python 3.11, asyncpg, SQLAlchemy 2.0
- **Frontend:** React 18, TypeScript, Vite
- **Database:** PostgreSQL 16 + pgvector
- **Local LLM:** Ollama (llama3.2)
- **Cloud LLM:** Anthropic (Claude)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Ollama (installed locally on host)

## Local Setup

### 1. Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Ensure `LLM_PROVIDER=ollama` is set.

### 2. Database (PostgreSQL + pgvector)
Start the database using Docker Compose:
```bash
docker compose up -d db
```

For a fresh database, apply the versioned schema after PostgreSQL is healthy:
```bash
python -m alembic -c backend/alembic.ini upgrade head
```
The FastAPI startup check still enables the `vector` extension and calls
`create_all()` for local resilience. Alembic is the migration authority for
schema changes and should be run before deploying a changed schema.

### 3. Ollama (Local LLM)
Ensure Ollama is running on your machine and pull the required model:
```bash
ollama pull llama3.2
```

### 4. Backend Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r backend/requirements.txt
```

### 5. Transcript Ingestion
From the project root, run the ingestion script to populate the database with the sample transcripts:
```bash
python scripts/ingest_transcripts.py
```
The script discovers `data/transcripts/*.md`, stores project-relative source paths, and skips an episode already indexed by title. Embeddings are generated with the configured real embedding provider before the source transaction is committed.

### 6. Run the Backend
```bash
uvicorn backend.app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 7. Run the Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
The application will be available at `http://localhost:5173`.

### Dockerized backend
The Compose backend uses the same application image and the CPU-only Torch
wheel, so `docker compose up --build` can start PostgreSQL and FastAPI without
pulling a GPU-enabled Torch distribution. Ollama remains a host service and is
reached from the container through `host.docker.internal`.

### Fresh database initialization
On backend startup, `init_database()` enables the PostgreSQL `vector` extension and creates missing SQLAlchemy tables, including the 384-dimensional pgvector embedding column. For a genuinely fresh install, apply the Alembic revision first or use a new PostgreSQL database:
```bash
docker compose down -v
docker compose up -d db
```
Then start the backend and run transcript ingestion. Do not substitute SQLite or in-memory storage: retrieval requires PostgreSQL plus pgvector.

## Live Verification (2026-09-13)

✅ Verified live on Windows: Docker Desktop, the Compose PostgreSQL + pgvector service, application table initialization, `vector(384)` schema, five-transcript ingestion, duplicate skipping, real pgvector retrieval, Ollama chat generation with `llama3.2`, Ollama embeddings with `all-minilm`, backend API flow, artifact persistence/reload, knowledge endpoints, frontend rendering, and API error handling.

⚠️ Verified statically: Anthropic provider selection and missing-key behavior. No Anthropic API key was configured, so no cloud request was made.

The default local embedding model is `all-MiniLM-L6-v2` and the compatible Ollama embedding option is `all-minilm`; both produce 384-dimensional vectors for the current schema.

✅ The full backend Docker image build completed successfully with the CPU-only Torch wheel, and `docker compose up -d --build` started both the backend and database services.

The Ollama provider uses a 300-second configurable timeout for CPU inference, and artifact generation is bounded to 600 tokens so the local artifact workflow completes reliably.

## Deployment (Vercel + Supabase)
1. **Database:** Create a Supabase project, enable the `vector` extension, and run the `init_db` logic.
2. **Backend:** Deploy the root directory to Vercel. Vercel will use `vercel.json` and `api/index.py` to deploy the FastAPI app as a Serverless Function.
3. **Frontend:** Deploy the `frontend/` directory to Vercel (Vite preset). Set the API URL to point to your backend deployment.
4. **Environment:** Set `LLM_PROVIDER=anthropic`, `ANTHROPIC_API_KEY`, and the Supabase `DATABASE_URL` in Vercel environment variables.

## Security
- **Sandboxed Iframes:** HTML artifacts are rendered using `<iframe sandbox="allow-scripts">` to prevent XSS and DOM access.
- **No Secrets in Logs:** Structured logging is configured to never log API keys or sensitive user payloads.
- **SQL Injection Prevention:** SQLAlchemy ORM and parameterized queries are used exclusively.
