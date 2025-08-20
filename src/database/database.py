"""
Database Connection
SQLAlchemy database connection and session management.
"""

import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self, database_url: str = "sqlite:///./name_generation.db"):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        
    def initialize(self):
        """Initialize database connection and create tables."""
        try:
            # Create engine
            if self.database_url.startswith("sqlite"):
                self.engine = create_engine(
                    self.database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool
                )
            else:
                self.engine = create_engine(self.database_url)
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            
            logger.info(f"Database initialized: {self.database_url}")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False
    
    def get_session(self) -> Session:
        """Get a database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self.SessionLocal()
    
    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Session:
    """Get database session for dependency injection."""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


def initialize_database(database_url: str = None) -> bool:
    """Initialize the database."""
    if database_url:
        db_manager.database_url = database_url
    return db_manager.initialize()


def close_database():
    """Close the database connection."""
    db_manager.close()
