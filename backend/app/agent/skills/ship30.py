from typing import List, Dict, Any, Tuple, Optional
from backend.app.llm.provider import LLMProvider
from backend.app.agent.tools.grounded import generate_grounded_answer
from backend.app.schemas.api import SourceInfo, ArtifactResponse
import uuid
from datetime import datetime

async def generate_ship30_essay(
    provider: LLMProvider,
    chunks: List[Dict[str, Any]],
    topic: str,
    conversation_history: List[Dict[str, Any]]
) -> Tuple[str, List[SourceInfo], Dict[str, Any]]:
    messages = conversation_history + [{"role": "user", "content": f"Write an essay about: {topic}"}]
    answer, sources = await generate_grounded_answer(provider, chunks, messages, "ship30")
    
    artifact = {
        "id": uuid.uuid4(),
        "type": "markdown",
        "title": f"Ship30 Essay: {topic[:20]}...",
        "content": answer,
        "created_at": datetime.utcnow()
    }
    
    msg = "I've drafted a Ship30-style essay based on the context. Check the artifact for the full text."
    return msg, sources, artifact
