"""
Database Session

Provides a request-scoped SQLAlchemy session for FastAPI route handlers
via dependency injection, plus an init_db() helper used on application
startup to create tables.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.db.database import Base, SessionLocal, engine

# Import models so they are registered on Base.metadata before create_all
# is called. Without this import, init_db() would create an empty schema.
from backend.app.db import models  # noqa: F401


def init_db() -> None:
    """Create all tables that don't already exist."""

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a request-scoped session."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
