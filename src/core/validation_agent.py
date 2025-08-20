"""
Validation Agent
Validates generated identities for cultural appropriateness and accuracy.
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from .models import IdentityRequest, ValidationResult
from .ethnicity_mapper import EthnicityMapper

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of identity validation."""
    is_valid: bool
    notes: List[str]
    cultural_score: float  # 0.0 to 1.0, higher is more culturally appropriate


class ValidationAgent:
    """Agent that validates generated identities."""
    
    def __init__(self):
        self.ethnicity_mapper = EthnicityMapper()
        self.cultural_validation_rules = self._initialize_validation_rules()
        
    def validate_identity(self, name_candidate: Dict[str, Any], 
                         request: IdentityRequest, 
                         cultural_context: Dict[str, Any]) -> ValidationResult:
        """
        Validate a name candidate for cultural appropriateness.
        
        Args:
            name_candidate: Generated name candidate
            request: Original identity request
            cultural_context: Cultural context information
            
        Returns:
            ValidationResult with validation status and notes
        """
        logger.info(f"Validating name candidate: {name_candidate}")
        
        validation_notes = []
        cultural_score = 1.0
        
        # Get ethnicity information
        ethnicity_info = self.ethnicity_mapper.get_ethnicity_info(request.race)
        
        # Check cultural appropriateness
        cultural_check = self._check_cultural_appropriateness(
            name_candidate, request.race, ethnicity_info, cultural_context
        )
        validation_notes.extend(cultural_check['notes'])
        cultural_score *= cultural_check['score']
        
        # Check naming conventions
        convention_check = self._check_naming_conventions(
            name_candidate, cultural_context
        )
        validation_notes.extend(convention_check['notes'])
        cultural_score *= convention_check['score']
        
        # Check for culturally inappropriate combinations
        inappropriate_check = self._check_inappropriate_combinations(
            name_candidate, request.race, ethnicity_info
        )
        validation_notes.extend(inappropriate_check['notes'])
        cultural_score *= inappropriate_check['score']
        
        # Determine if valid based on cultural score
        is_valid = cultural_score >= 0.7  # Require 70% cultural appropriateness
        
        if cultural_score < 0.7:
            validation_notes.append(
                f"Culturally inappropriate: score {cultural_score:.2f} < 0.7"
            )
        
        result = ValidationResult(
            is_valid=is_valid,
            notes=validation_notes,
            cultural_score=cultural_score
        )
        
        logger.info(f"Validation result: {result}")
        return result
    
    def _check_cultural_appropriateness(self, name_candidate: Dict[str, Any],
                                      race: str, ethnicity_info: Any,
                                      cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if names are culturally appropriate for the ethnicity."""
        notes = []
        score = 1.0
        
        if not ethnicity_info:
            notes.append("No ethnicity information available for validation")
            return {'notes': notes, 'score': 0.5}
        
        first_name = name_candidate.get('first_name', '').lower()
        last_name = name_candidate.get('last_name', '').lower()
        middle_name = name_candidate.get('middle_name')
        
        # Check for culturally inappropriate Western names for non-Western ethnicities
        western_first_names = [
            'david', 'thomas', 'william', 'joseph', 'michael', 'christopher',
            'james', 'robert', 'john', 'daniel', 'marie', 'faith', 'grace',
            'elizabeth', 'sarah', 'jessica', 'ashley', 'amanda'
        ]
        
        western_last_names = [
            'rodriguez', 'williams', 'smith', 'davis', 'johnson', 'brown',
            'jones', 'garcia', 'miller', 'wilson', 'martinez', 'anderson'
        ]
        
        race_lower = race.lower()
        
        # For Southeast Asian ethnicities, reject Western names
        if race_lower in ['cambodian', 'khmer', 'thai', 'vietnamese']:
            if first_name in western_first_names:
                notes.append(f"Western first name '{first_name}' inappropriate for {race}")
                score *= 0.1  # Severe penalty
            
            if last_name in western_last_names:
                notes.append(f"Western last name '{last_name}' inappropriate for {race}")
                score *= 0.1  # Severe penalty
        
        # For East Asian ethnicities, reject Western names
        elif race_lower in ['korean', 'japanese', 'chinese']:
            if first_name in western_first_names:
                notes.append(f"Western first name '{first_name}' inappropriate for {race}")
                score *= 0.2  # Significant penalty
            
            if last_name in western_last_names:
                notes.append(f"Western last name '{last_name}' inappropriate for {race}")
                score *= 0.2  # Significant penalty
        
        # Check for middle names when culture doesn't support them
        if middle_name and not cultural_context.get('supports_middle_names'):
            notes.append(f"Middle name '{middle_name}' not appropriate for {race} culture")
            score *= 0.8
        
        return {'notes': notes, 'score': score}
    
    def _check_naming_conventions(self, name_candidate: Dict[str, Any],
                                cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if naming conventions are followed."""
        notes = []
        score = 1.0
        
        first_name = name_candidate.get('first_name', '')
        last_name = name_candidate.get('last_name', '')
        middle_name = name_candidate.get('middle_name')
        
        # Check for empty names
        if not first_name or not last_name:
            notes.append("Missing first or last name")
            score *= 0.0
        
        # Check naming order
        naming_order = cultural_context.get('naming_order', 'first-last')
        if naming_order == 'last-first' and ' ' in last_name:
            # For cultures with surname first, check if surname is properly formatted
            pass  # Could add more specific checks here
        
        return {'notes': notes, 'score': score}
    
    def _check_inappropriate_combinations(self, name_candidate: Dict[str, Any],
                                        race: str, ethnicity_info: Any) -> Dict[str, Any]:
        """Check for culturally inappropriate name combinations."""
        notes = []
        score = 1.0
        
        if not ethnicity_info:
            return {'notes': notes, 'score': score}
        
        first_name = name_candidate.get('first_name', '').lower()
        last_name = name_candidate.get('last_name', '').lower()
        
        # Check for specific inappropriate combinations
        race_lower = race.lower()
        
        # Cambodian/Khmer specific checks
        if race_lower in ['cambodian', 'khmer']:
            # Reject Western names for Cambodian ethnicity
            western_names = ['david', 'thomas', 'william', 'joseph', 'marie', 'faith']
            western_surnames = ['rodriguez', 'williams', 'smith', 'davis']
            
            if first_name in western_names:
                notes.append(f"Western first name '{first_name}' inappropriate for Cambodian")
                score *= 0.0  # Complete rejection
            
            if last_name in western_surnames:
                notes.append(f"Western surname '{last_name}' inappropriate for Cambodian")
                score *= 0.0  # Complete rejection
            
            # Check for typical Khmer name patterns
            khmer_first_names = ['sopheak', 'sokha', 'rithy', 'sambath', 'sophea']
            khmer_surnames = ['sok', 'sopheak', 'rithy', 'sambath']
            
            if first_name not in khmer_first_names and last_name not in khmer_surnames:
                notes.append("Name doesn't follow typical Khmer naming patterns")
                score *= 0.3
        
        return {'notes': notes, 'score': score}
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize cultural validation rules."""
        return {
            'southeast_asian': {
                'no_western_names': True,
                'no_middle_names': True,
                'traditional_names_required': True
            },
            'east_asian': {
                'no_western_names': True,
                'no_middle_names': True,
                'surname_first': True
            },
            'south_asian': {
                'middle_names_allowed': True,
                'traditional_names_preferred': True
            },
            'middle_eastern': {
                'middle_names_allowed': True,
                'patronymic_system': True
            },
            'european': {
                'middle_names_allowed': True,
                'flexible_naming': True
            },
            'african': {
                'middle_names_allowed': True,
                'traditional_names_preferred': True
            },
            'american': {
                'flexible_naming': True,
                'western_names_allowed': True
            }
        }
