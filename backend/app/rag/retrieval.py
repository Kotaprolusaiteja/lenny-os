from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from backend.app.db.models import TranscriptChunk, TranscriptSource
from backend.app.rag.embeddings import generate_embedding

async def search_similar_chunks(session: AsyncSession, query: str, top_k: int) -> List[Dict[str, Any]]:
    if top_k < 1:
        return []
    query_embedding = await generate_embedding(query)
    
    distance_expr = TranscriptChunk.embedding.cosine_distance(query_embedding)
    stmt = (
        select(TranscriptChunk, TranscriptSource, distance_expr.label("distance"))
        .join(TranscriptSource)
        .order_by(distance_expr)
        .limit(top_k)
    )
    
    result = await session.execute(stmt)
    rows = result.all()
    
    results = []
    for chunk, source, distance in rows:
        results.append({
            "content": chunk.content,
            "metadata": chunk.metadata_,
            "score": 1.0 - distance,
            "source": {
                "episode": source.episode_title,
                "guest": source.guest,
                "path": source.source_path,
                "url": source.source_url,
                "date": source.date
            }
        })
    return results

async def get_source_count(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(TranscriptSource.id)))
    return result.scalar_one()

async def get_chunk_count(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(TranscriptChunk.id)))
    return result.scalar_one()
