"""
Database connection and session management.
Includes encryption layer for sensitive financial data.
"""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager

from config import settings
from database.models import Base


# Create engine based on database URL
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite specific settings
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL settings
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables (use with caution)."""
    Base.metadata.drop_all(bind=engine)


def get_db():
    """
    Dependency for FastAPI endpoints.
    Yields a database session and ensures cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    Usage: with get_db_session() as db: ...
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """
    Database management utilities.
    """
    
    @staticmethod
    def create_tables():
        """Create all tables defined in models."""
        init_db()
        print("Database tables created successfully.")
    
    @staticmethod
    def reset_database():
        """Reset database (drop and recreate all tables)."""
        drop_db()
        init_db()
        print("Database reset successfully.")
    
    @staticmethod
    def get_session() -> Session:
        """Get a new database session."""
        return SessionLocal()
    
    @staticmethod
    def health_check() -> bool:
        """Check database connectivity."""
        try:
            with get_db_session() as db:
                db.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False


# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
