"""
Database Models
SQLAlchemy models for the name generation system.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Phase 1: New Identity Generation System Models

class Identity(Base):
    """Core identity table for Phase 1."""
    __tablename__ = "identities"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    sex = Column(String(20), nullable=False)  # Male, Female, Non-binary
    location = Column(String(100), nullable=False)  # Country and region
    age = Column(Integer, nullable=False)
    occupation = Column(String(200), nullable=False)
    race = Column(String(100), nullable=False)  # Cultural and ethnic background
    religion = Column(String(100), nullable=False)
    birth_year = Column(Integer, nullable=False)
    generated_date = Column(DateTime, default=datetime.utcnow)
    is_accepted = Column(Boolean, default=False)
    accepted_date = Column(DateTime, nullable=True)
    validation_status = Column(String(20), default='pending')  # pending, validated, rejected
    
    # Relationships
    validation_results = relationship("ValidationResult", back_populates="identity")


class WatchlistEntry(Base):
    """Watchlist entries for criminal/terrorist validation."""
    __tablename__ = "watchlist_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    source = Column(String(100), nullable=False)  # OFAC, FBI, Interpol, etc.
    reason = Column(Text, nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class ValidationResult(Base):
    """Validation results for identities."""
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    identity_id = Column(Integer, ForeignKey("identities.id"), nullable=False)
    watchlist_check = Column(Boolean, nullable=True)
    accepted_names_check = Column(Boolean, nullable=True)
    validation_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    
    # Relationships
    identity = relationship("Identity", back_populates="validation_results")


class AcceptedName(Base):
    """Accepted names to prevent reuse."""
    __tablename__ = "accepted_names"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    accepted_date = Column(DateTime, default=datetime.utcnow)
    original_identity_id = Column(Integer, ForeignKey("identities.id"), nullable=True)


class AvoidedName(Base):
    """Names to avoid for cultural, religious, or other reasons."""
    __tablename__ = "avoided_names"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    reason = Column(Text, nullable=False)  # Cultural, religious, offensive, etc.
    culture = Column(String(100), nullable=True)  # Specific culture if applicable
    religion = Column(String(100), nullable=True)  # Specific religion if applicable
    region = Column(String(100), nullable=True)  # Specific region if applicable
    added_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class CulturalNamingRule(Base):
    """Cultural naming rules and conventions."""
    __tablename__ = "cultural_naming_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    culture = Column(String(100), nullable=False, index=True)
    region = Column(String(100), nullable=True, index=True)
    religion = Column(String(100), nullable=True, index=True)
    rule_type = Column(String(50), nullable=False)  # patronymic, matronymic, compound, etc.
    description = Column(Text, nullable=False)
    requires_mother_name = Column(Boolean, default=False)
    requires_father_name = Column(Boolean, default=False)
    supports_hyphenation = Column(Boolean, default=False)
    naming_order = Column(String(50), nullable=True)  # first-last, last-first, etc.
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)


# Legacy models for backward compatibility (Phase 2+)

class Category(Base):
    """Name categories table."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    names = relationship("Name", back_populates="category")


class Name(Base):
    """Generated names table."""
    __tablename__ = "names"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    generated_date = Column(DateTime, default=datetime.utcnow)
    parameters_used = Column(Text, nullable=True)  # JSON string
    is_validated = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="names")


class UserSession(Base):
    """User sessions table."""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    parameters = Column(Text, nullable=True)  # JSON string
    is_active = Column(Boolean, default=True)


class Watchlist(Base):
    """Watchlists and exclusion lists table."""
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    pattern = Column(String(255), nullable=False, index=True)
    category = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
