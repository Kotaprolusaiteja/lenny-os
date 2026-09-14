from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.rag.retrieval import search_similar_chunks

async def retrieve_knowledge(session: AsyncSession, query: str, top_k: int) -> List[Dict[str, Any]]:
    return await search_similar_chunks(session, query, top_k)
