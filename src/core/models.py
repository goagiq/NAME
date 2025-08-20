"""
Data models for the core identity generation system.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class IdentityRequest:
    """Request for identity generation."""
    sex: str
    location: str
    age: int
    occupation: str
    race: str
    religion: str
    birth_year: int
    birth_country: Optional[str] = None  # Country of birth/origin
    citizenship_country: Optional[str] = None  # Current citizenship
    diaspora_generation: Optional[int] = None  # 1st, 2nd, 3rd gen immigrant


@dataclass
class GeneratedIdentity:
    """Generated identity with validation results."""
    first_name: str
    middle_name: Optional[str]
    last_name: str
    cultural_context: Dict[str, Any]
    validation_status: str
    validation_notes: List[str]
    generated_date: datetime = None
    detailed_traceability: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.generated_date is None:
            self.generated_date = datetime.utcnow()


@dataclass
class CulturalContext:
    """Cultural context information for name generation."""
    culture: str
    region: str
    language: str
    religion: str
    naming_conventions: Dict[str, Any]
    special_requirements: List[str]
    naming_order: str
    supports_middle_names: bool
    supports_hyphenation: bool
    requires_patronymic: bool
    requires_matronymic: bool


@dataclass
class ValidationResult:
    """Result of name validation."""
    is_valid: bool
    notes: List[str]
    watchlist_check: bool
    accepted_names_check: bool
    avoided_names_check: bool
    cultural_acceptability_check: bool
    special_requirements_check: bool
