from typing import List, Dict, Any
from backend.app.schemas.api import SourceInfo

PROMPTS = {
    "default": "You are a helpful AI assistant. Answer using ONLY the provided context. Do not fabricate info. Cite sources. If not enough info, say so.",
    "ship30": "You are a writing assistant. Write a ~1250 word essay based on the context using the Ship30 formatting. Cite sources.",
    "artifact": "You are a document generation assistant. Create the requested artifact using ONLY the context provided.",
    "challenge": "You are a critical thinking assistant. Challenge the user's assumptions based on the evidence provided in the context."
}

def build_context(chunks: List[Dict[str, Any]]) -> str:
    parts = []
    for i, c in enumerate(chunks):
        parts.append(f"[Source {i+1}]: Episode '{c['source']['episode']}'\n{c['content']}")
    return "\n\n".join(parts)

def build_system_prompt(chunks: List[Dict[str, Any]], prompt_type: str) -> str:
    base_prompt = PROMPTS.get(prompt_type, PROMPTS["default"])
    context_str = build_context(chunks)
    return f"{base_prompt}\n\nCONTEXT:\n{context_str}"

def build_sources_response(chunks: List[Dict[str, Any]]) -> List[SourceInfo]:
    seen_episodes = set()
    sources = []
    for c in chunks:
        ep = c["source"]["episode"]
        if ep not in seen_episodes:
            seen_episodes.add(ep)
            sources.append(SourceInfo(
                episode=ep,
                guest=c["source"]["guest"],
                source=c["source"]["path"],
                relevance=c.get("score", 0.9),
                content_snippet=c["content"][:200] + "..."
            ))
            if len(sources) >= 4:
                break
    return sources
