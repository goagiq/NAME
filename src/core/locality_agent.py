"""
Locality Agent
Understands culture, ethnicity, language, and religion for specific regions.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .models import IdentityRequest
from .ethnicity_mapper import EthnicityMapper

logger = logging.getLogger(__name__)


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
    country_of_origin: str
    diaspora_generation: Optional[int] = None


class LocalityAgent:
    """Agent that analyzes cultural context for name generation."""
    
    def __init__(self):
        self.cultural_database = self._initialize_cultural_database()
        self.ethnicity_mapper = EthnicityMapper()
        
    def analyze_cultural_context(self, request: IdentityRequest) -> Dict[str, Any]:
        """
        Analyze cultural context based on user parameters.
        
        Args:
            request: IdentityRequest with user parameters
            
        Returns:
            Dictionary with cultural context information
        """
        logger.info(f"Analyzing cultural context for {request.location}, "
                   f"{request.race}, {request.religion}")
        
        # Extract location components
        country, region = self._parse_location(request.location)
        
        # Get ethnicity information
        ethnicity_info = self.ethnicity_mapper.get_ethnicity_info(request.race)
        
        # Auto-detect country of origin if not provided
        birth_country = request.birth_country
        if not birth_country and ethnicity_info:
            birth_country = ethnicity_info.primary_country
            logger.info(f"Auto-detected country of origin: {birth_country}")
        
        # Get cultural context with enhanced ethnicity mapping
        cultural_context = self._get_cultural_context(
            country, region, request.race, request.religion, 
            ethnicity_info, birth_country, request.diaspora_generation
        )
        
        # Add special requirements based on culture and religion
        special_requirements = self._get_special_requirements(
            cultural_context, request
        )
        
        # Determine naming conventions
        naming_conventions = self._get_naming_conventions(cultural_context)
        
        result = {
            'culture': cultural_context.culture,
            'region': cultural_context.region,
            'language': cultural_context.language,
            'religion': cultural_context.religion,
            'naming_conventions': naming_conventions,
            'special_requirements': special_requirements,
            'naming_order': cultural_context.naming_order,
            'supports_middle_names': cultural_context.supports_middle_names,
            'supports_hyphenation': cultural_context.supports_hyphenation,
            'requires_patronymic': cultural_context.requires_patronymic,
            'requires_matronymic': cultural_context.requires_matronymic,
            'country_of_origin': cultural_context.country_of_origin,
            'diaspora_generation': cultural_context.diaspora_generation,
            'regional_context': cultural_context.naming_conventions.get('regional_context', False),
            'sub_region': cultural_context.naming_conventions.get('sub_region', None)
        }
        
        logger.info(f"Cultural context result: {result}")
        return result
    
    def _get_special_requirements_for_culture(self, culture: str) -> List[str]:
        """Get special requirements for a given culture."""
        requirements_map = {
            'Cambodian': ['khmer_naming_convention', 'respect_royal_names'],
            'Thai': ['thai_naming_convention', 'respect_royal_names'],
            'Vietnamese': ['vietnamese_naming_convention'],
            'Korean': ['korean_naming_convention', 'generational_consideration'],
            'Japanese': ['japanese_naming_convention', 'kanji_consideration'],
            'Chinese': ['chinese_naming_convention', 'generational_consideration'],
            'Indian': ['indian_naming_convention', 'caste_consideration'],
            'Arabic': ['arabic_naming_convention', 'religious_consideration'],
            'Persian': ['persian_naming_convention', 'poetic_consideration'],
            'Turkish': ['turkish_naming_convention', 'ottoman_influence'],
            'Italian': ['italian_naming_convention', 'regional_variations'],
            'French': ['french_naming_convention', 'regional_variations'],
            'Spanish': ['spanish_naming_convention', 'maternal_paternal_surnames'],
            'Russian': ['russian_naming_convention', 'patronymic_system'],
            'Polish': ['polish_naming_convention', 'patronymic_system'],
            'Swedish': ['swedish_naming_convention', 'patronymic_system'],
            'German': ['german_naming_convention', 'regional_variations'],
            'African American': ['african_american_naming_convention', 'cultural_revival'],
            'Nigerian': ['nigerian_naming_convention', 'tribal_consideration'],
            'American': ['american_naming_convention', 'flexible_naming']
        }
        return requirements_map.get(culture, ['general_naming_convention'])
    
    def _get_naming_order_for_culture(self, culture: str) -> str:
        """Get naming order for a given culture."""
        order_map = {
            'Cambodian': 'first-last',
            'Thai': 'first-last',
            'Vietnamese': 'last-first',
            'Korean': 'last-first',
            'Japanese': 'last-first',
            'Chinese': 'last-first',
            'Indian': 'first-last',
            'Arabic': 'first-last',
            'Persian': 'first-last',
            'Turkish': 'first-last',
            'Italian': 'first-last',
            'French': 'first-last',
            'Spanish': 'first-last',
            'Russian': 'first-last',
            'Polish': 'first-last',
            'Swedish': 'first-last',
            'German': 'first-last',
            'African American': 'first-last',
            'Nigerian': 'first-last',
            'American': 'first-last'
        }
        return order_map.get(culture, 'first-last')
    
    def _parse_location(self, location: str) -> tuple[str, str]:
        """Parse location into country and region."""
        parts = location.split(',')
        country = parts[0].strip()
        region = parts[1].strip() if len(parts) > 1 else ""
        return country, region
    
    def _get_cultural_context(self, country: str, region: str, 
                            race: str, religion: str,
                            ethnicity_info: Optional[Any], birth_country: Optional[str], diaspora_generation: Optional[int]) -> CulturalContext:
        """Get cultural context from database."""
        
        # Use ethnicity info if available (this includes regional modifiers)
        if ethnicity_info:
            culture = ethnicity_info.culture
            language = ethnicity_info.language
            primary_region = ethnicity_info.region
            naming_conventions = ethnicity_info.naming_conventions
            
            # Check if this is a regional variant
            regional_context = naming_conventions.get('regional_context', False)
            sub_region = naming_conventions.get('sub_region', None)
            
            return CulturalContext(
                culture=culture,
                region=sub_region or primary_region,
                language=language,
                religion=religion,
                naming_conventions=naming_conventions,
                special_requirements=self._get_special_requirements_for_culture(culture),
                naming_order=self._get_naming_order_for_culture(culture),
                supports_middle_names=naming_conventions.get('uses_middle_names', True),
                supports_hyphenation=naming_conventions.get('supports_hyphenation', False),
                requires_patronymic=naming_conventions.get('requires_patronymic', False),
                requires_matronymic=naming_conventions.get('requires_matronymic', False),
                country_of_origin=birth_country or ethnicity_info.primary_country,
                diaspora_generation=diaspora_generation
            )
        
        # Fallback to hardcoded logic for backward compatibility
        race_lower = race.lower()
        if race_lower in ['cambodian', 'khmer']:
            return CulturalContext(
                culture="Cambodian",
                region=region or country,
                language="Khmer",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "no_middle_names": True,
                    "traditional_khmer_names": True,
                    "uses_titles": True,
                    "royal_names": True
                },
                special_requirements=["khmer_naming_convention", "respect_royal_names"],
                naming_order="first-last",
                supports_middle_names=False,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Cambodia",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['thai', 'thailand']:
            return CulturalContext(
                culture="Thai",
                region=region or country,
                language="Thai",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "no_middle_names": True,
                    "traditional_thai_names": True,
                    "uses_titles": True,
                    "royal_names": True
                },
                special_requirements=["thai_naming_convention", "respect_royal_names"],
                naming_order="first-last",
                supports_middle_names=False,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Thailand",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['vietnamese', 'vietnam']:
            return CulturalContext(
                culture="Vietnamese",
                region=region or country,
                language="Vietnamese",
                religion=religion,
                naming_conventions={
                    "surname_first": True,
                    "no_middle_names": True,
                    "traditional_vietnamese_names": True,
                    "uses_titles": False
                },
                special_requirements=["vietnamese_naming_convention"],
                naming_order="last-first",
                supports_middle_names=False,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Vietnam",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['korean', 'korea']:
            return CulturalContext(
                culture="Korean",
                region=region or country,
                language="Korean",
                religion=religion,
                naming_conventions={
                    "surname_first": True,
                    "no_middle_names": True,
                    "traditional_korean_names": True,
                    "uses_titles": False,
                    "generational_names": True
                },
                special_requirements=["korean_naming_convention", "generational_consideration"],
                naming_order="last-first",
                supports_middle_names=False,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "South Korea",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['japanese', 'japan']:
            return CulturalContext(
                culture="Japanese",
                region=region or country,
                language="Japanese",
                religion=religion,
                naming_conventions={
                    "surname_first": True,
                    "no_middle_names": True,
                    "traditional_japanese_names": True,
                    "uses_titles": False,
                    "kanji_names": True
                },
                special_requirements=["japanese_naming_convention", "kanji_consideration"],
                naming_order="last-first",
                supports_middle_names=False,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Japan",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['filipino', 'philippines', 'filipina']:
            return CulturalContext(
                culture="Filipino",
                region=region or country,
                language="Tagalog/English",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_filipino_names": True,
                    "spanish_influence": True
                },
                special_requirements=["filipino_naming_convention", "spanish_influence"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Philippines",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['indian', 'india', 'hindu', 'sikh', 'muslim_indian']:
            return CulturalContext(
                culture="Indian",
                region=region or country,
                language="Multiple (Hindi, Tamil, Bengali, etc.)",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_indian_names": True,
                    "caste_consideration": True,
                    "regional_variations": True
                },
                special_requirements=["indian_naming_convention", "caste_consideration", "regional_variations"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "India",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['arabic', 'middle_eastern', 'lebanese', 'syrian', 'egyptian', 'saudi']:
            return CulturalContext(
                culture="Arabic",
                region=region or country,
                language="Arabic",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_arabic_names": True,
                    "patronymic_system": True,
                    "religious_names": True
                },
                special_requirements=["arabic_naming_convention", "religious_consideration", "patronymic_system"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=False,
                requires_patronymic=True,
                requires_matronymic=False,
                country_of_origin=birth_country or "Middle East",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['persian', 'iranian', 'iran']:
            return CulturalContext(
                culture="Persian",
                region=region or country,
                language="Persian",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_persian_names": True,
                    "royal_names": True,
                    "poetic_names": True
                },
                special_requirements=["persian_naming_convention", "royal_names", "poetic_consideration"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Iran",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['turkish', 'turkey']:
            return CulturalContext(
                culture="Turkish",
                region=region or country,
                language="Turkish",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_turkish_names": True,
                    "ottoman_influence": True
                },
                special_requirements=["turkish_naming_convention", "ottoman_influence"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=False,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Turkey",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['african_american', 'black_american']:
            return CulturalContext(
                culture="African American",
                region=region or country,
                language="English",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "modern_african_american_names": True,
                    "creative_names": True,
                    "cultural_revival": True
                },
                special_requirements=["african_american_naming_convention", "cultural_revival"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "United States",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['nigerian', 'ghanaian', 'kenyan', 'ethiopian', 'south_african']:
            return CulturalContext(
                culture="African",
                region=region or country,
                language="Multiple (English, French, Portuguese, etc.)",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_african_names": True,
                    "tribal_names": True,
                    "colonial_influence": True
                },
                special_requirements=["african_naming_convention", "tribal_consideration"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Africa",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['russian', 'ukrainian', 'polish', 'czech', 'slovak']:
            return CulturalContext(
                culture="Eastern European",
                region=region or country,
                language="Slavic Languages",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_slavic_names": True,
                    "patronymic_system": True,
                    "diminutive_names": True
                },
                special_requirements=["slavic_naming_convention", "patronymic_system"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=False,
                requires_patronymic=True,
                requires_matronymic=False,
                country_of_origin=birth_country or "Eastern Europe",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['swedish', 'norwegian', 'danish', 'finnish', 'icelandic']:
            return CulturalContext(
                culture="Scandinavian",
                region=region or country,
                language="Scandinavian Languages",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_scandinavian_names": True,
                    "patronymic_system": True,
                    "nature_names": True
                },
                special_requirements=["scandinavian_naming_convention", "patronymic_system"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=False,
                requires_patronymic=True,
                requires_matronymic=False,
                country_of_origin=birth_country or "Scandinavia",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['italian', 'italy']:
            return CulturalContext(
                culture="Italian",
                region=region or country,
                language="Italian",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_italian_names": True,
                    "regional_variations": True,
                    "saint_names": True
                },
                special_requirements=["italian_naming_convention", "regional_variations", "saint_names"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Italy",
                diaspora_generation=diaspora_generation
            )
        elif race_lower in ['french', 'france']:
            return CulturalContext(
                culture="French",
                region=region or country,
                language="French",
                religion=religion,
                naming_conventions={
                    "surname_first": False,
                    "uses_middle_names": True,
                    "traditional_french_names": True,
                    "regional_variations": True,
                    "aristocratic_names": True
                },
                special_requirements=["french_naming_convention", "regional_variations"],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "France",
                diaspora_generation=diaspora_generation
            )
        elif country.lower() == "spain":
            return CulturalContext(
                culture="Spanish",
                region=region or "Spain",
                language="Spanish",
                religion=religion,
                naming_conventions={
                    "uses_multiple_middle_names": True,
                    "maternal_paternal_surnames": True,
                    "formal_naming": True
                },
                special_requirements=[],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Spain",
                diaspora_generation=diaspora_generation
            )
        elif country.lower() == "united states":
            return CulturalContext(
                culture="American",
                region=region or "United States",
                language="English",
                religion=religion,
                naming_conventions={
                    "uses_single_middle_name": True,
                    "various_ethnic_patterns": True,
                    "flexible_naming": True
                },
                special_requirements=[],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "United States",
                diaspora_generation=diaspora_generation
            )
        else:
            # Default context
            return CulturalContext(
                culture=race,
                region=region or country,
                language="English",
                religion=religion,
                naming_conventions={
                    "standard_naming": True
                },
                special_requirements=[],
                naming_order="first-middle-last",
                supports_middle_names=True,
                supports_hyphenation=True,
                requires_patronymic=False,
                requires_matronymic=False,
                country_of_origin=birth_country or "Unknown",
                diaspora_generation=diaspora_generation
            )
    
    def _get_special_requirements(self, context: CulturalContext, 
                                request: IdentityRequest) -> List[str]:
        """Get special naming requirements based on culture and religion."""
        requirements = []
        
        # Religious requirements
        if request.religion.lower() == "islam":
            requirements.append("avoid_names_of_false_gods")
            requirements.append("prefer_islamic_names")
        elif request.religion.lower() == "judaism":
            requirements.append("consider_hebrew_names")
            requirements.append("avoid_graven_images")
        
        # Cultural requirements
        if context.culture.lower() == "spanish":
            requirements.append("multiple_middle_names")
            requirements.append("maternal_paternal_surnames")
        elif context.culture.lower() == "chinese":
            requirements.append("surname_first")
            requirements.append("generational_names")
        
        return requirements
    
    def _get_naming_conventions(self, context: CulturalContext) -> Dict[str, Any]:
        """Get specific naming conventions for the culture."""
        return context.naming_conventions
    
    def _initialize_cultural_database(self) -> Dict[str, Any]:
        """Initialize cultural database with naming rules."""
        # This would load from the cultural_naming_rules table
        return {
            "spain": {
                "naming_order": "first-middle-last",
                "supports_middle_names": True,
                "supports_hyphenation": True,
                "requires_patronymic": False,
                "requires_matronymic": False,
                "special_features": ["multiple_middle_names", "maternal_paternal_surnames"]
            },
            "united_states": {
                "naming_order": "first-middle-last",
                "supports_middle_names": True,
                "supports_hyphenation": True,
                "requires_patronymic": False,
                "requires_matronymic": False,
                "special_features": ["various_ethnic_patterns", "flexible_naming"]
            }
        }
