# Demo Script

**Estimated Time:** 2.5 Minutes

### Step 1: Open App & Landing Page (0:00 - 0:20)
*   **Action:** Open `http://localhost:5173` in browser.
*   **Talk Track:** "This is Lenny OS, the Lenny Growth Assistant. We've designed this not as a generic chatbot, but as a premium workspace for product intelligence. The landing page greets you with actionable quick prompts."

### Step 2: Ask a Product Question (0:20 - 0:45)
*   **Action:** Click the "How do great teams improve onboarding?" prompt.
*   **Talk Track:** "When we ask a question, the system queries a local PostgreSQL database with pgvector, fetching only relevant transcript segments from the Lenny Podcast corpus."

### Step 3: Show Grounded Answer & Evidence (0:45 - 1:15)
*   **Action:** Point out the "HOW THIS ANSWER WAS BUILT" transparency card, and the Evidence source cards below the text.
*   **Talk Track:** "Notice the transparency card—it shows the exact retrieval metrics. We don't hide the RAG process. Below the response, you see the exact sources used, attributing Lauryn Isford from episode 42. Every claim in the text maps back to this evidence."

### Step 4: Show Ollama Status (1:15 - 1:30)
*   **Action:** Point to the top right status indicator `● LOCAL Ollama · llama3.2`.
*   **Talk Track:** "Everything you're seeing right now is running entirely locally via Ollama and sentence-transformers for embeddings. No cloud APIs are being used. We can switch to Anthropic simply by flipping an environment variable."

### Step 5: Artifact Generation (1:30 - 2:00)
*   **Action:** Type: "Create a 30-day onboarding plan using this evidence."
*   **Talk Track:** "The assistant has a specialized Artifact skill. When it detects an artifact request, it changes its system prompt and output format."
*   **Action:** Watch the right-hand Artifact Viewer slide in.
*   **Talk Track:** "It opens the generated markdown artifact side-by-side with the chat. This viewer also securely renders HTML artifacts in a sandboxed iframe if we asked for a visual template."

### Step 6: Ship 30 Studio (2:00 - 2:30)
*   **Action:** Click "Ship 30 Studio" button in the UI, or type "Write a Ship 30 essay about growth loops."
*   **Talk Track:** "We also built a specialized workflow for writing. This invokes a different skill in the agent layer that strictly enforces a ~1,250 word output with proper hooks, pacing, and source attribution."

## Live Verification Status

✅ This flow was exercised live on 2026-09-13 with the Compose PostgreSQL + pgvector service, five indexed transcripts, Ollama `llama3.2`, and the Vite frontend. The question returned grounded evidence, artifact generation persisted across session reload, and the browser rendered the answer, sources, transparency data, and artifact viewer.

⚠️ The current sample corpus contains five supplied transcripts, not hundreds of episodes. Anthropic was not live-tested because no API key was configured.

⚠️ The backend was run directly from the project virtual environment for this live demo. The Compose database passed; the full backend image build remained in Torch dependency installation and was not claimed as passed.
