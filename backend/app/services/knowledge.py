from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.db.models import TranscriptChunk, TranscriptSource

async def get_themes(db: AsyncSession) -> dict:
    themes = ["Product", "Growth", "Leadership", "Hiring", "Strategy", "Career"]
    # We do not have predefined theme tags in the schema, so we initialize to 0. 
    # A full implementation would query metadata or full-text search.
    source_count = await db.scalar(select(func.count(TranscriptSource.id)))
    return [{"name": theme, "description": "", "source_count": source_count or 0} for theme in themes]

async def get_sources(db: AsyncSession) -> list[dict]:
    stmt = (
        select(TranscriptSource, func.count(TranscriptChunk.id))
        .outerjoin(TranscriptChunk, TranscriptChunk.source_id == TranscriptSource.id)
        .group_by(TranscriptSource.id)
        .order_by(TranscriptSource.created_at.desc())
    )
    result = await db.execute(stmt)
    return [{
        "id": source.id,
        "episode_title": source.episode_title,
        "guest": source.guest,
        "episode_number": source.episode_number,
        "source_url": source.source_url,
        "date": source.date,
        "chunk_count": chunk_count,
    } for source, chunk_count in result.all()]
