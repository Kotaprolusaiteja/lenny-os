import os
import re
import yaml
import asyncio
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.engine import get_session
from backend.app.db.models import TranscriptSource, TranscriptChunk
from backend.app.rag.embeddings import generate_embeddings_batch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "transcripts")

def parse_markdown(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        text = parts[2].strip()
    else:
        frontmatter = {}
        text = content.strip()
        
    return {
        "metadata": frontmatter,
        "content": re.sub(r'\s+', ' ', text)
    }

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        if i > 0 and len(words) - i <= overlap:
            break
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

async def process_file(filepath: str, session: AsyncSession):
    parsed = parse_markdown(filepath)
    meta = parsed["metadata"]
    content = parsed["content"]
    
    title = meta.get("title", os.path.basename(filepath))
    
    # Check duplicate
    stmt = select(TranscriptSource).where(TranscriptSource.episode_title == title)
    res = await session.execute(stmt)
    if res.scalar_one_or_none():
        print(f"Skipping duplicate: {title}")
        return
        
    source = TranscriptSource(
        episode_title=title,
        guest=meta.get("guest"),
        source_path=os.path.relpath(filepath, PROJECT_ROOT),
        source_url=meta.get("source_url"),
        episode_number=meta.get("episode_number"),
        date=str(meta.get("date")) if meta.get("date") else None
    )
    text_chunks = chunk_text(content)
    if not text_chunks:
        return
        
    # generate embeddings
    embeddings = await generate_embeddings_batch(text_chunks)

    if len(embeddings) != len(text_chunks):
        raise ValueError(f"Expected {len(text_chunks)} embeddings, got {len(embeddings)}")

    session.add(source)
    await session.flush()
    
    for i, (text_chunk, emb) in enumerate(zip(text_chunks, embeddings)):
        db_chunk = TranscriptChunk(
            source_id=source.id,
            content=text_chunk,
            embedding=emb,
            chunk_index=i,
            metadata_={"title": title}
        )
        session.add(db_chunk)
        
    await session.commit()
    print(f"Ingested {title} ({len(text_chunks)} chunks)")

async def main():
    if not os.path.exists(DATA_DIR):
        print(f"Data dir not found: {DATA_DIR}")
        return
        
    md_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".md")]
    print(f"Found {len(md_files)} files to ingest.")
    
    async for session in get_session():
        for f in md_files:
            await process_file(f, session)
        break

if __name__ == "__main__":
    asyncio.run(main())
