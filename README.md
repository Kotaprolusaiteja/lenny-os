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
- **Local LLM:** Ollama (`llama3.2`)
- **Cloud LLM:** Anthropic (Claude)
- **Embeddings:** 384-dimensional embeddings
  - **Local:** Ollama (`all-minilm`) / sentence-transformers (`all-MiniLM-L6-v2`)
  - **Cloud:** Configurable embedding provider

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
