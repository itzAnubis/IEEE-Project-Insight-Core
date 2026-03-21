"""
Database engine, session factory, initialization, and seed data.

- Creates a SQLite database at ./database/sessions.db
- Tables are auto-created on startup via init_db()
- seed_data() inserts a sample session (id=1) if not already present
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.models import Base, Session

logger = logging.getLogger("api.db")

# ---------------------------------------------------------------------------
# Database path — relative to the project root
# ---------------------------------------------------------------------------
DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "sessions.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite with threads
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables if they do not exist."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized — all tables created (if not existing)")


def seed_data():
    """Insert sample session id=1 if the sessions table is empty."""
    db = SessionLocal()
    try:
        existing = db.query(Session).filter(Session.id == 1).first()
        if existing is None:
            sample_session = Session(
                id=1,
                title="Introduction to Machine Learning",
                instructor_name="Dr. Sarah Ahmed",
                status="idle",
            )
            db.add(sample_session)
            db.commit()
            logger.info("Seed data inserted — session id=1 created")
        else:
            logger.info("Seed data skipped — session id=1 already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Seed data error: {e}")
    finally:
        db.close()
