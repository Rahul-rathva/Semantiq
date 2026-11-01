from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_pgvector_extension() -> None:
    """Ensure pgvector extension exists for PostgreSQL databases."""
    if not settings.database_url.startswith("postgresql"):
        return

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
