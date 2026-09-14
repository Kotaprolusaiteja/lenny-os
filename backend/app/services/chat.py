import time
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.api import ChatResponse, ChatMetadata, ArtifactResponse
from backend.app.core.errors import AppError, ErrorCode
from backend.app.services.session import add_message, get_session_messages, get_session_detail
from backend.app.agent.router import detect_intent
from backend.app.llm.anthropic import get_llm_provider
from backend.app.agent.tools.retrieval import retrieve_knowledge
from backend.app.config import settings
from backend.app.agent.tools.grounded import generate_grounded_answer
from backend.app.agent.skills.ship30 import generate_ship30_essay
from backend.app.agent.skills.artifact import generate_artifact

def serialize_artifact(artifact: dict | None) -> dict | None:
    if not artifact:
        return None
    return {
        **artifact,
        "id": str(artifact["id"]),
        "created_at": artifact["created_at"].isoformat(),
    }

async def process_chat(db: AsyncSession, session_id: str, user_message: str) -> ChatResponse:
    sess_detail = await get_session_detail(db, session_id)
    if not sess_detail:
        raise AppError(ErrorCode.SESSION_NOT_FOUND, "Session not found", 404)
        
    start_time = time.time()
    
    await add_message(db, session_id, "user", user_message)
    history = await get_session_messages(db, session_id, limit=10)
    
    intent = detect_intent(user_message)
    provider = get_llm_provider()
    
    chunks = await retrieve_knowledge(db, user_message, top_k=settings.retrieval_top_k)
    
    artifact = None
    if intent == "ship30":
        answer, sources, art = await generate_ship30_essay(provider, chunks, user_message, history[:-1])
        artifact = art
    elif intent == "artifact":
        answer, sources, art = await generate_artifact(provider, chunks, user_message, history[:-1])
        artifact = art
    elif intent == "challenge":
        answer, sources = await generate_grounded_answer(provider, chunks, history[:-1] + [{"role": "user", "content": user_message}], "challenge")
    else:
        answer, sources = await generate_grounded_answer(provider, chunks, history[:-1] + [{"role": "user", "content": user_message}], "qa")
        
    latency = (time.time() - start_time) * 1000
    
    metadata = ChatMetadata(
        retrieval_count=len(chunks),
        source_count=len(sources),
        latency_ms=latency,
        chunks_retrieved=len(chunks),
        provider=provider.provider_name(),
        model=provider.model_name()
    )
    
    stored_artifact = serialize_artifact(artifact)

    await add_message(
        db, 
        session_id, 
        "assistant", 
        answer, 
        sources=[s.dict() for s in sources] if sources else None,
        metadata=metadata.dict(),
        artifact=stored_artifact
    )
    
    resp_artifact = None
    if artifact:
        resp_artifact = ArtifactResponse(
            id=artifact["id"],
            type=artifact["type"],
            title=artifact["title"],
            content=artifact["content"],
            created_at=artifact["created_at"]
        )
        
    return ChatResponse(
        answer=answer,
        sources=sources,
        provider=provider.provider_name(),
        model=provider.model_name(),
        metadata=metadata,
        artifact=resp_artifact,
        wisdom_action=None,
        insight_map=None
    )
