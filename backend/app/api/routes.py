from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.app.api.deps import get_db
from backend.app.schemas.api import (
    HealthResponse, ReadyResponse, SessionResponse, SessionDetailResponse, ChatRequest, ChatResponse, CreateSessionRequest
)
from backend.app.db.engine import check_db_health
from backend.app.llm.anthropic import get_llm_provider
from backend.app.rag.retrieval import get_source_count, get_chunk_count
from backend.app.services.session import create_session, get_sessions, get_session_detail, delete_session
from backend.app.services.chat import process_chat
from backend.app.services.knowledge import get_themes, get_sources

router = APIRouter(prefix="/api")

@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_ok = await check_db_health()
    provider = get_llm_provider()
    llm_ok = await provider.health_check()
    sources = await get_source_count(db) if db_ok else 0
    chunks = await get_chunk_count(db) if db_ok else 0
    
    return HealthResponse(
        status="ok" if db_ok and llm_ok else "degraded",
        database=db_ok,
        llm_provider=provider.provider_name(),
        llm_available=llm_ok,
        embedding_available=True,
        indexed_sources=sources,
        indexed_chunks=chunks
    )

@router.get("/ready", response_model=ReadyResponse)
async def ready_check(db: AsyncSession = Depends(get_db)):
    db_ok = await check_db_health()
    provider = get_llm_provider()
    llm_ok = await provider.health_check()
    
    return ReadyResponse(
        ready=db_ok and llm_ok,
        checks={"database": db_ok, "llm": llm_ok}
    )

@router.post("/sessions", response_model=SessionResponse)
async def create_new_session(req: CreateSessionRequest, db: AsyncSession = Depends(get_db)):
    return await create_session(db, req.title)

@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    return await get_sessions(db)

@router.get("/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    sess = await get_session_detail(db, session_id)
    if not sess:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return sess

@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str, db: AsyncSession = Depends(get_db)):
    success = await delete_session(db, session_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    return await process_chat(db, request.session_id, request.message)

@router.get("/knowledge/themes")
async def list_themes(db: AsyncSession = Depends(get_db)):
    return await get_themes(db)

@router.get("/knowledge/sources")
async def list_sources(db: AsyncSession = Depends(get_db)):
    return await get_sources(db)
