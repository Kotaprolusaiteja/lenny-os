# Agent Transcript 01: Initial RAG Setup

## Objective
Establish a local PostgreSQL + pgvector RAG pipeline for the Lenny Growth Assistant.

## Prompt Summary
- Use the supplied podcast transcript markdown files.
- Preserve source metadata and return evidence with answers.
- Avoid duplicate transcript ingestion.

## Implementation
- Parsed YAML frontmatter from `data/transcripts/*.md`.
- Chunked transcripts into 512-word chunks with 64-word overlap.
- Generated 384-dimensional embeddings with `all-MiniLM-L6-v2`.
- Stored sources, chunks, metadata, and vectors in PostgreSQL with pgvector.
- Added a title-based duplicate check before inserting a source.

## Debugging Notes
An initial local verification checked the database schema, vector extension, and ingestion counts before running another ingestion pass. The duplicate pass skipped existing episode titles, leaving the index unchanged.

## Verification
- PostgreSQL + pgvector healthy.
- Five transcript sources indexed.
- Ten transcript chunks indexed.
- Cosine retrieval returned relevant evidence and source cards.

## Security Scrub
No API keys, passwords, tokens, personal data, or private URLs are recorded in this transcript.
