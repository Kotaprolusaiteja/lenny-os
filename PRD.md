# Product Requirements Document (PRD)

## 1. Discovery Brief
**Product Name:** Lenny OS — The Lenny Growth Assistant
**Positioning:** "Turn product wisdom into your next move."
**Overview:** A full-stack AI conversational application grounded entirely in Lenny's Podcast transcripts. Designed for product managers, founders, and growth leaders to extract actionable insights from industry experts.

## 2. User & Problem
**Target User:** Product Managers, Growth Engineers, Startup Founders
**Problem:** There is an overwhelming amount of high-quality product advice in Lenny's Podcast, but it is difficult to search, synthesize, and apply to specific company problems on demand.
**Job-to-be-Done:** "When I face a complex product decision, I want to instantly consult the synthesized wisdom of world-class product leaders so that I can make a grounded, confident choice."

## 3. Success Metrics
*   **TARGET:** 100% of claims made by the assistant must be grounded in the provided transcripts. (No hallucination).
*   **TARGET:** 95% of queries should return relevant transcript chunks (Assuming the query is within the domain of the transcripts).
*   **TARGET:** Assistant response time (including retrieval and generation) should be under 3 seconds for local (Ollama) and 2 seconds for cloud (Anthropic).
*   **ACTUAL MEASURED RESULT:** [To be updated after testing]

## 4. Scope & Features
### In Scope
-   RAG-based conversational AI.
-   Independent chat sessions with history context.
-   Ship 30 for 30 essay generation.
-   Artifact generation (Markdown/HTML) for growth plans, memos, etc.
-   Artifact Viewer with sandboxed HTML rendering.
-   "Wisdom → Action" and "Challenge My Thinking" structured workflows.
-   Dual LLM support (Local Ollama / Cloud Anthropic).
-   PostgreSQL / pgvector persistence.

### Non-Goals
-   Live web search.
-   User authentication/login (single-tenant local deployment for now).
-   Audio playback of the podcast.

## 5. User Flows
1.  **Landing:** User opens the app, sees "TURN PRODUCT WISDOM INTO YOUR NEXT MOVE" and clicks a quick prompt.
2.  **Q&A:** System retrieves transcripts, displays grounded answer, and shows evidence source cards.
3.  **Action:** User clicks "Create action plan" → System generates a Markdown artifact → Artifact Viewer opens on the right.
4.  **Ship 30:** User types "Write a Ship 30 essay about onboarding" → System generates a 1,250-word essay with strict formatting.

## 6. Requirements
-   **Backend:** FastAPI, Python 3.11+.
-   **Database:** PostgreSQL with pgvector extension.
-   **Frontend:** React 18, TypeScript, Vite.
-   **LLM Abstraction:** Must switch cleanly between Ollama and Anthropic based on `.env`.
-   **Vector Search:** Cosine similarity via pgvector.
-   **Security:** HTML artifacts must render in a sandboxed iframe.

## 7. Risks & Trade-offs
-   **Risk:** Local LLM (llama3.2) may struggle with long context windows compared to Claude.
-   **Trade-off:** We use smaller, 512-word chunks to accommodate local model context limits while maintaining high relevance.
-   **Trade-off:** Using `sentence-transformers` locally instead of Ollama embeddings ensures embedding works consistently regardless of which LLM is running, making the Vercel deployment easier (since Vercel doesn't have local Ollama).

## 8. Operational Assumptions & Safety
-   **Deployment shape:** The default install is a single-tenant local deployment. Authentication and tenant isolation are intentionally out of scope.
-   **Inference:** CPU Ollama inference is supported and can take several minutes. The provider timeout is configurable and defaults to 300 seconds; cloud Anthropic requests use the SDK timeout behavior.
-   **Context:** Retrieval returns the six highest-scoring 512-word chunks with 64-word overlap. The grounding prompt limits answers to that evidence and asks the model to state when evidence is insufficient.
-   **Data leakage:** Secrets are read from environment configuration, excluded from logs and transcript evidence, and never included in prompts unless a user explicitly types them. Local persistence is limited to the configured PostgreSQL instance.
-   **Hallucination mitigation:** Every answer is generated with retrieved transcript context, source metadata is returned beside the answer, and the system prompt requires an explicit insufficient-evidence response instead of unsupported claims.
-   **Untrusted HTML:** Generated HTML is displayed only in an iframe with `sandbox="allow-scripts"`; it has no same-origin access to the application document.

## 9. Implementation Plan
-   Phase 1: Database & RAG setup (pgvector).
-   Phase 2: FastAPI backend & LLM Provider abstraction.
-   Phase 3: Agent Layer (Tools & Skills).
-   Phase 4: Frontend UI & State Management.
-   Phase 5: Integration, Dockerization, and Testing.
