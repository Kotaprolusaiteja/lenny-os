# Submission Checklist

| Requirement | Implementation Details | Status |
| :--- | :--- | :---: |
| **Backend & Architecture** | | |
| FastAPI | `backend/app/main.py` and `backend/app/api/routes.py` | [x] |
| Independent sessions | `backend/app/services/session.py` (UUID session IDs) | [x] |
| PostgreSQL | `backend/app/db/engine.py` (asyncpg) | [x] |
| LLM configuration | `backend/app/config.py` + `backend/app/llm/provider.py` | [x] |
| Cloud provider / Claude Agent SDK boundary | `backend/app/llm/anthropic.py` + `backend/app/agent/execution.py` | [x] |
| Ollama | `backend/app/llm/ollama.py` | [x] |
| **RAG Pipeline** | | |
| Transcript ingestion | `scripts/ingest_transcripts.py` | [x] |
| Chunking/indexing | `chunk_text()` (512 words / 64 overlap) + pgvector | [x] |
| Retrieval | `backend/app/rag/retrieval.py` (cosine similarity) | [x] |
| Source grounding | `backend/app/rag/context.py` (strict system prompts) | [x] |
| Insufficient-evidence | Enforced in `SYSTEM_PROMPT` ("I don't have enough evidence") | [x] |
| **Agent Layer** | | |
| Agent routing | `backend/app/agent/router.py` (intent detection) | [x] |
| Ship30 skill | `backend/app/agent/skills/ship30.py` | [x] |
| ~1,250-word output | `max_tokens=6000` + prompt constraint | [x] |
| Markdown artifact | `backend/app/agent/skills/artifact.py` | [x] |
| HTML/CSS artifact | `backend/app/agent/skills/artifact.py` | [x] |
| **Frontend UI** | | |
| Artifact Viewer | `frontend/src/components/ArtifactViewer.tsx` | [x] |
| HTML isolation | `iframe sandbox="allow-scripts"` | [x] |
| Responsive | CSS Media Queries in `index.css` | [x] |
| **Operations** | | |
| Docker | `docker-compose.yml` | [x] |
| `.env.example` | Included | [x] |
| Structured logs | `backend/app/core/logging.py` (structlog) | [x] |
| Error handling | `backend/app/core/errors.py` (AppError / ErrorCode) | [x] |
| Resilience | Timeouts, ConnectErrors, ProviderError handling | [x] |
| **Documentation** | | |
| README | Evaluator-quality `README.md` | [x] |
| PRD | `PRD.md` | [x] |
| design.md | `design.md` | [x] |
| architecture.md | `architecture.md` | [x] |
| agent transcripts | `agent_transcripts/01_initial_rag_setup.md`, `02_agent_routing_debug.md`, `03_docker_fix_and_verification.md` | [x] |
| demo documentation | `DEMO.md` | [x] |
| Vercel compatibility| `vercel.json` and `api/index.py` | [x] |

## Verification Status

✅ **Verified live:** Docker Desktop, the PostgreSQL + pgvector Compose service, vector extension, all six tables, `vector(384)`, five sources, ten embedded chunks, metadata persistence, duplicate ingestion handling, real cosine retrieval, Ollama `llama3.2`, Ollama `all-minilm` embeddings, FastAPI health/readiness/session/chat/knowledge/error routes, artifact persistence/reload, and browser rendering.

✅ **Automated tests:** 12 passed, 0 failed in `backend/tests/test_quality_gate.py`.

⚠️ **Frontend lint:** No separate lint command is defined; `npm run build` completed its TypeScript check successfully.

⚠️ **Static only:** Anthropic provider contract and missing-key behavior. No API key was configured, so no Anthropic request was made. The explicit Claude SDK execution boundary is covered by code inspection and deterministic provider tests.

✅ **Migrations:** Alembic is initialized under `backend/alembic` with an initial revision covering all six SQLAlchemy models. `alembic upgrade head` is documented and offline SQL generation passed.

✅ **Container build:** Requirements pin the CPU-only Torch wheel and the Dockerfile uses cache-friendly dependency installation. Compose backend/database integration is covered by the final verification command.
