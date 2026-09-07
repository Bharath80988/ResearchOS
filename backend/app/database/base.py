import uuid
from datetime import datetime, timezone
from typing import Generator
from sqlalchemy import create_engine, DateTime, String
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, Mapped, mapped_column
from ..config import get_settings
from ..utils import logger

settings = get_settings()

def get_engine(db_url: str = None):
    url = db_url or settings.DATABASE_URL
    try:
        engine = create_engine(
            url,
            pool_pre_ping=True,
            echo=False
        )
        # Test connection quickly
        with engine.connect():
            pass
        return engine
    except Exception as e:
        logger.warning(f"Could not connect to configured database at {url}: {e}")
        logger.info("Falling back to local SQLite database for development.")
        fallback_url = "sqlite:///./researchos_dev.db"
        return create_engine(fallback_url, connect_args={"check_same_thread": False})

engine = get_engine()
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


class BaseModel(Base):
    """Abstract base model with standard UUID primary key and timestamp tracking."""
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


def get_db() -> Generator:
    """Dependency helper yielding scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(target_engine=None):
    """Initializes all registered table schemas."""
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)
    logger.info("Database schemas initialized successfully.")
