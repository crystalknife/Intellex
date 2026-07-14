"""
Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from backend.app.config import settings

_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    # SQLite connections are single-threaded by default; the scheduler
    # runs ingestion on a background thread separate from request
    # handling, so this needs to be relaxed for local/dev SQLite use.
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    # Recycle dead Postgres connections instead of surfacing a stale
    # connection error to the caller.
    pool_pre_ping=not _is_sqlite,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass