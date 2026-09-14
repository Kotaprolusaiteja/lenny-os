import asyncio
from sqlalchemy import text
from backend.app.db.engine import engine
from backend.app.db.models import Base

async def init_database():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
