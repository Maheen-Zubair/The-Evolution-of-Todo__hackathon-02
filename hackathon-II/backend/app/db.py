"""
Phase 2 Full-Stack Todo App - Database Configuration

Neon PostgreSQL connection and session management using SQLModel.
"""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling for Neon
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENVIRONMENT") == "development",  # Log SQL in dev
    pool_pre_ping=True,  # Check connection before use
    pool_recycle=300,  # Recycle connections after 5 minutes
)


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields a SQLModel session that automatically closes after use.
    Use with FastAPI's Depends() for dependency injection.

    Example:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            return session.exec(select(Item)).all()
    """
    with Session(engine) as session:
        yield session
