from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, max_length=10000)

class CreateSessionRequest(BaseModel):
    title: Optional[str] = None

class SourceInfo(BaseModel):
    episode: str
    guest: Optional[str] = None
    source: str
    relevance: float
    content_snippet: str

class ArtifactResponse(BaseModel):
    id: uuid.UUID
    type: str
    title: str
    content: str
    created_at: datetime

class WisdomAction(BaseModel):
    evidence_suggests: str
    what_it_means: str
    what_to_do_next: str

class InsightMap(BaseModel):
    topic: str
    themes: List[str]
    episodes: List[str]
    takeaway: str

class ChatMetadata(BaseModel):
    retrieval_count: int
    source_count: int
    latency_ms: float
    chunks_retrieved: int
    provider: str
    model: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    provider: str
    model: str
    metadata: ChatMetadata
    artifact: Optional[ArtifactResponse] = None
    wisdom_action: Optional[WisdomAction] = None
    insight_map: Optional[InsightMap] = None

class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    sources: Optional[List[SourceInfo]] = None
    metadata: Optional[Dict[str, Any]] = None
    artifact: Optional[ArtifactResponse] = None
    created_at: datetime

class SessionResponse(BaseModel):
    id: uuid.UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse]

class HealthResponse(BaseModel):
    status: str
    database: bool
    llm_provider: str
    llm_available: bool
    embedding_available: bool
    indexed_sources: int
    indexed_chunks: int

class ReadyResponse(BaseModel):
    ready: bool
    checks: Dict[str, bool]
