from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import Session, Message
from backend.app.schemas.api import SessionResponse, SessionDetailResponse, MessageResponse
import uuid

async def create_session(db: AsyncSession, title: str = None) -> SessionResponse:
    db_session = Session(title=title)
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return SessionResponse(
        id=db_session.id,
        title=db_session.title,
        created_at=db_session.created_at,
        updated_at=db_session.updated_at,
        message_count=0
    )

async def get_sessions(db: AsyncSession) -> list[SessionResponse]:
    stmt = (
        select(Session, func.count(Message.id).label("msg_count"))
        .outerjoin(Message)
        .group_by(Session.id)
        .order_by(Session.updated_at.desc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        SessionResponse(
            id=sess.id,
            title=sess.title,
            created_at=sess.created_at,
            updated_at=sess.updated_at,
            message_count=count
        )
        for sess, count in rows
    ]

async def get_session_detail(db: AsyncSession, session_id: str) -> SessionDetailResponse:
    try:
        parsed_id = uuid.UUID(session_id)
    except ValueError:
        return None
    stmt = select(Session).where(Session.id == parsed_id)
    result = await db.execute(stmt)
    sess = result.scalar_one_or_none()
    if not sess:
        return None
        
    msg_stmt = select(Message).where(Message.session_id == sess.id).order_by(Message.created_at)
    msg_result = await db.execute(msg_stmt)
    messages = msg_result.scalars().all()
    
    msg_responses = [
        MessageResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            sources=m.sources,
            metadata=m.metadata_,
            artifact=m.artifact,
            created_at=m.created_at
        ) for m in messages
    ]
    
    return SessionDetailResponse(
        id=sess.id,
        title=sess.title,
        created_at=sess.created_at,
        updated_at=sess.updated_at,
        message_count=len(messages),
        messages=msg_responses
    )

async def delete_session(db: AsyncSession, session_id: str) -> bool:
    try:
        parsed_id = uuid.UUID(session_id)
    except ValueError:
        return False
    stmt = select(Session).where(Session.id == parsed_id)
    result = await db.execute(stmt)
    sess = result.scalar_one_or_none()
    if sess:
        await db.delete(sess)
        await db.commit()
        return True
    return False

async def add_message(db: AsyncSession, session_id: str, role: str, content: str, sources: list = None, metadata: dict = None, artifact: dict = None) -> Message:
    stmt = select(Session).where(Session.id == uuid.UUID(session_id))
    result = await db.execute(stmt)
    sess = result.scalar_one()
    
    if role == "user" and (sess.title is None or sess.title == ""):
        sess.title = content[:50] + "..." if len(content) > 50 else content
        
    msg = Message(
        session_id=sess.id,
        role=role,
        content=content,
        sources=sources,
        metadata_=metadata,
        artifact=artifact
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_session_messages(db: AsyncSession, session_id: str, limit: int = 10) -> list[dict]:
    stmt = select(Message).where(Message.session_id == uuid.UUID(session_id)).order_by(Message.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return [{"role": m.role, "content": m.content} for m in reversed(messages)]
