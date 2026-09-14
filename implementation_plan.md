# Implementation Plan

## Runtime Architecture

1. Start PostgreSQL with the `pgvector/pgvector:pg16` Compose service.
2. Initialize the `vector` extension and SQLAlchemy tables on FastAPI startup.
3. Ingest `data/transcripts/*.md` by parsing frontmatter, chunking transcript text, generating 384-dimensional embeddings, and storing source metadata and chunks.
4. Retrieve relevant chunks with PostgreSQL pgvector cosine-distance ordering.
5. Build a grounded context prompt and route generation through the configured Ollama or Anthropic provider.
6. Persist sessions, messages, sources, metadata, and generated artifacts in PostgreSQL.
7. Serve the React/Vite frontend through the API proxy and render evidence and artifacts in the workspace UI.

## Verification Plan

- Run the deterministic backend suite with `\.venv\Scripts\python.exe -m pytest -q`.
- Run Python compile/import checks.
- Run `npm run build` in `frontend`.
- Start Compose PostgreSQL and verify pgvector, tables, `vector(384)`, ingestion counts, and duplicate handling.
- Start Ollama with `llama3.2` and `all-minilm`, then verify health, embeddings, grounded chat, artifact generation, and session reload.
- Open the frontend and verify session creation, question answering, evidence, artifact viewer, and API error handling.

## Current State

The implementation is complete and was live-verified on 2026-09-13. PostgreSQL/pgvector, Ollama, FastAPI, and Vite were exercised locally. Anthropic remains statically verified only because no API key was configured. No migration framework is included; fresh databases use startup initialization.
