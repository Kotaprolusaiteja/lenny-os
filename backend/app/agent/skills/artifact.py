import re
import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple
from backend.app.llm.provider import LLMProvider
from backend.app.agent.tools.grounded import generate_grounded_answer
from backend.app.schemas.api import SourceInfo

def detect_artifact_type(message: str) -> str:
    if "html" in message.lower() or "website" in message.lower():
        return "html"
    return "markdown"

def extract_artifact_title(message: str) -> str:
    # Very simple extraction
    return "Generated Artifact"

async def generate_artifact(
    provider: LLMProvider,
    chunks: List[Dict[str, Any]],
    message: str,
    conversation_history: List[Dict[str, Any]]
) -> Tuple[str, List[SourceInfo], Dict[str, Any]]:
    messages = conversation_history + [{"role": "user", "content": message}]
    answer, sources = await generate_grounded_answer(
        provider,
        chunks,
        messages,
        "artifact",
        max_tokens=600,
    )
    
    art_type = detect_artifact_type(message)
    title = extract_artifact_title(message)
    
    artifact = {
        "id": uuid.uuid4(),
        "type": art_type,
        "title": title,
        "content": answer,
        "created_at": datetime.utcnow()
    }
    
    return "I have created the requested artifact. Please review it.", sources, artifact
