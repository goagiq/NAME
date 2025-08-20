"""
Ethnicity Mapping System
Comprehensive mapping of ethnicities to countries, cultures, and regions.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

@dataclass
class EthnicityInfo:
    """Information about an ethnicity."""
    ethnicity: str
    primary_country: str
    region: str
    culture: str
    language: str
    alternative_names: List[str]
    diaspora_patterns: List[str]
    naming_conventions: Dict[str, Any]


class EthnicityMapper:
    """Maps ethnicities to countries, cultures, and regions."""
    
    def __init__(self):
        self.ethnicity_database = self._initialize_ethnicity_database()
        self.regional_modifiers = self._initialize_regional_modifiers()
    
    def get_ethnicity_info(self, ethnicity: str) -> Optional[EthnicityInfo]:
        """Get comprehensive information about an ethnicity."""
        ethnicity_lower = ethnicity.lower().strip()
        
        # Check for regional modifiers first
        primary_ethnicity, sub_region = self._resolve_regional_modifier(ethnicity_lower)
        if primary_ethnicity:
            base_info = self.ethnicity_database.get(primary_ethnicity)
            if base_info:
                # Create enhanced info with regional context
                return self._create_regional_ethnicity_info(base_info, sub_region)
        
        # Direct match
        if ethnicity_lower in self.ethnicity_database:
            return self.ethnicity_database[ethnicity_lower]
        
        # Alternative name match
        for info in self.ethnicity_database.values():
            if ethnicity_lower in [alt.lower() for alt in info.alternative_names]:
                return info
        
        return None
    
    def _resolve_regional_modifier(self, ethnicity: str) -> Tuple[Optional[str], Optional[str]]:
        """Resolve regional modifiers to primary ethnicities."""
        for modifier, (primary, region) in self.regional_modifiers.items():
            if ethnicity.startswith(modifier) or ethnicity.endswith(modifier):
                return primary, region
        return None, None
    
    def _create_regional_ethnicity_info(self, base_info: EthnicityInfo, sub_region: str) -> EthnicityInfo:
        """Create enhanced ethnicity info with regional context."""
        # Create a copy with regional enhancements
        regional_info = EthnicityInfo(
            ethnicity=f"{sub_region} {base_info.ethnicity}",
            primary_country=base_info.primary_country,
            region=base_info.region,
            culture=base_info.culture,
            language=base_info.language,
            alternative_names=base_info.alternative_names + [sub_region.lower()],
            diaspora_patterns=base_info.diaspora_patterns,
            naming_conventions={
                **base_info.naming_conventions,
                'sub_region': sub_region,
                'regional_context': True
            }
        )
        return regional_info
    
    def get_country_of_origin(self, ethnicity: str) -> Optional[str]:
        """Get the primary country of origin for an ethnicity."""
        info = self.get_ethnicity_info(ethnicity)
        return info.primary_country if info else None
    
    def get_cultural_roots(self, ethnicity: str) -> Optional[str]:
        """Get the cultural root/identity for an ethnicity."""
        info = self.get_ethnicity_info(ethnicity)
        return info.culture if info else None
    
    def get_region(self, ethnicity: str) -> Optional[str]:
        """Get the geographical region for an ethnicity."""
        info = self.get_ethnicity_info(ethnicity)
        return info.region if info else None
    
    def _initialize_regional_modifiers(self) -> Dict[str, Tuple[str, str]]:
        """Initialize regional modifiers that map to primary ethnicities."""
        return {
            # Indian regional modifiers
            'south indian': ('indian', 'South India'),
            'north indian': ('indian', 'North India'),
            'bengali': ('indian', 'Bengal'),
            'tamil': ('indian', 'Tamil Nadu'),
            'telugu': ('indian', 'Andhra Pradesh'),
            'malayalam': ('indian', 'Kerala'),
            'kannada': ('indian', 'Karnataka'),
            'marathi': ('indian', 'Maharashtra'),
            'gujarati': ('indian', 'Gujarat'),
            'punjabi': ('indian', 'Punjab'),
            'rajasthani': ('indian', 'Rajasthan'),
            'bihari': ('indian', 'Bihar'),
            'oriya': ('indian', 'Odisha'),
            'assamese': ('indian', 'Assam'),
            
            # Chinese regional modifiers
            'mandarin': ('chinese', 'Northern China'),
            'cantonese': ('chinese', 'Southern China'),
            'hakka': ('chinese', 'Hakka Region'),
            'hokkien': ('chinese', 'Fujian'),
            'shanghainese': ('chinese', 'Shanghai'),
            'sichuanese': ('chinese', 'Sichuan'),
            'taiwanese': ('chinese', 'Taiwan'),
            
            # Korean regional modifiers
            'seoul': ('korean', 'Seoul'),
            'busan': ('korean', 'Busan'),
            'jeju': ('korean', 'Jeju'),
            
            # Japanese regional modifiers
            'tokyo': ('japanese', 'Tokyo'),
            'osaka': ('japanese', 'Osaka'),
            'kyoto': ('japanese', 'Kyoto'),
            'hokkaido': ('japanese', 'Hokkaido'),
            
            # Italian regional modifiers
            'southern italian': ('italian', 'Southern Italy'),
            'northern italian': ('italian', 'Northern Italy'),
            'sicilian': ('italian', 'Sicily'),
            'sardinian': ('italian', 'Sardinia'),
            'venetian': ('italian', 'Veneto'),
            'tuscan': ('italian', 'Tuscany'),
            
            # French regional modifiers
            'parisian': ('french', 'Paris'),
            'provencal': ('french', 'Provence'),
            'breton': ('french', 'Brittany'),
            'alsatian': ('french', 'Alsace'),
            'norman': ('french', 'Normandy'),
            
            # Spanish regional modifiers
            'castilian': ('spanish', 'Castile'),
            'catalan': ('spanish', 'Catalonia'),
            'andalusian': ('spanish', 'Andalusia'),
            'basque': ('spanish', 'Basque Country'),
            'galician': ('spanish', 'Galicia'),
            
            # German regional modifiers
            'bavarian': ('german', 'Bavaria'),
            'saxon': ('german', 'Saxony'),
            'prussian': ('german', 'Prussia'),
            'swabian': ('german', 'Swabia'),
            'rhinelander': ('german', 'Rhineland'),
            
            # Russian regional modifiers
            'muscovite': ('russian', 'Moscow'),
            'siberian': ('russian', 'Siberia'),
            'ural': ('russian', 'Urals'),
            'caucasian': ('russian', 'Caucasus'),
            
            # Turkish regional modifiers
            'istanbul': ('turkish', 'Istanbul'),
            'anatolian': ('turkish', 'Anatolia'),
            'aegean': ('turkish', 'Aegean'),
            'black sea': ('turkish', 'Black Sea'),
            
            # Arabic regional modifiers
            'egyptian': ('arabic', 'Egypt'),
            'lebanese': ('arabic', 'Lebanon'),
            'syrian': ('arabic', 'Syria'),
            'saudi': ('arabic', 'Saudi Arabia'),
            'iraqi': ('arabic', 'Iraq'),
            'jordanian': ('arabic', 'Jordan'),
            'palestinian': ('arabic', 'Palestine'),
            'moroccan': ('arabic', 'Morocco'),
            'tunisian': ('arabic', 'Tunisia'),
            'algerian': ('arabic', 'Algeria'),
            
            # Vietnamese regional modifiers
            'hanoi': ('vietnamese', 'Hanoi'),
            'saigon': ('vietnamese', 'Ho Chi Minh City'),
            'hue': ('vietnamese', 'Hue'),
            
            # Thai regional modifiers
            'bangkok': ('thai', 'Bangkok'),
            'chiang mai': ('thai', 'Chiang Mai'),
            'phuket': ('thai', 'Phuket'),
            
            # Filipino regional modifiers
            'tagalog': ('filipino', 'Luzon'),
            'cebuano': ('filipino', 'Cebu'),
            'ilocano': ('filipino', 'Ilocos'),
            'bicolano': ('filipino', 'Bicol'),
            
            # African regional modifiers
            'yoruba': ('nigerian', 'Yoruba'),
            'igbo': ('nigerian', 'Igbo'),
            'hausa': ('nigerian', 'Hausa'),
            'fulani': ('nigerian', 'Fulani'),
        }
    
    def _initialize_ethnicity_database(self) -> Dict[str, EthnicityInfo]:
        """Initialize comprehensive ethnicity database."""
        return {
            # Southeast Asian
            'cambodian': EthnicityInfo(
                ethnicity='Cambodian',
                primary_country='Cambodia',
                region='Southeast Asia',
                culture='Khmer',
                language='Khmer',
                alternative_names=['khmer', 'cambodia'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'traditional_khmer_names': True,
                    'surname_patterns': ['sok', 'sopheak', 'rithy', 'sambath']
                }
            ),
            'thai': EthnicityInfo(
                ethnicity='Thai',
                primary_country='Thailand',
                region='Southeast Asia',
                culture='Thai',
                language='Thai',
                alternative_names=['thailand', 'siamese'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'traditional_thai_names': True,
                    'royal_names': True
                }
            ),
            'vietnamese': EthnicityInfo(
                ethnicity='Vietnamese',
                primary_country='Vietnam',
                region='Southeast Asia',
                culture='Vietnamese',
                language='Vietnamese',
                alternative_names=['vietnam'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'surname_first': True,
                    'traditional_vietnamese_names': True
                }
            ),
            'filipino': EthnicityInfo(
                ethnicity='Filipino',
                primary_country='Philippines',
                region='Southeast Asia',
                culture='Filipino',
                language='Tagalog/English',
                alternative_names=['philippines', 'filipina'],
                diaspora_patterns=['traditional', 'spanish_influenced', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'spanish_influence': True
                }
            ),
            
            # East Asian
            'korean': EthnicityInfo(
                ethnicity='Korean',
                primary_country='Korea',
                region='East Asia',
                culture='Korean',
                language='Korean',
                alternative_names=['korea', 'south korean'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'surname_first': True,
                    'generational_names': True
                }
            ),
            'japanese': EthnicityInfo(
                ethnicity='Japanese',
                primary_country='Japan',
                region='East Asia',
                culture='Japanese',
                language='Japanese',
                alternative_names=['japan'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'surname_first': True,
                    'kanji_names': True
                }
            ),
            'chinese': EthnicityInfo(
                ethnicity='Chinese',
                primary_country='China',
                region='East Asia',
                culture='Chinese',
                language='Mandarin/Cantonese',
                alternative_names=['china', 'mandarin', 'cantonese', 'taiwanese'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'no_middle_names': True,
                    'surname_first': True,
                    'generational_names': True,
                    'taiwanese_names': ['wei-chen', 'jia-ling', 'yu-ting', 'pei-chi', 'hsiao-wei', 'chun-hui'],
                    'taiwanese_surnames': ['chen', 'lin', 'wang', 'liu', 'yang', 'huang', 'wu', 'tsai']
                }
            ),
            
            # South Asian
            'indian': EthnicityInfo(
                ethnicity='Indian',
                primary_country='India',
                region='South Asia',
                culture='Indian',
                language='Multiple (Hindi, Tamil, Bengali, etc.)',
                alternative_names=['india', 'hindu', 'sikh', 'muslim_indian'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'caste_consideration': True,
                    'regional_variations': True,
                    'south_indian_names': ['priya', 'lakshmi', 'meenakshi', 'saraswati', 'parvati', 'gayatri'],
                    'south_indian_surnames': ['iyer', 'iyengar', 'pillai', 'chettiar', 'mudaliar', 'reddy', 'naidu'],
                    'north_indian_names': ['arjun', 'vikram', 'rahul', 'priya', 'amit', 'raj'],
                    'north_indian_surnames': ['sharma', 'verma', 'patel', 'singh', 'kumar', 'gupta']
                }
            ),
            
            # Middle Eastern
            'arabic': EthnicityInfo(
                ethnicity='Arabic',
                primary_country='Various (Lebanon, Syria, Egypt, Saudi Arabia)',
                region='Middle East',
                culture='Arabic',
                language='Arabic',
                alternative_names=['middle_eastern', 'lebanese', 'syrian', 'egyptian', 'saudi'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'patronymic_system': True,
                    'religious_names': True
                }
            ),
            'persian': EthnicityInfo(
                ethnicity='Persian',
                primary_country='Iran',
                region='Middle East',
                culture='Persian',
                language='Persian',
                alternative_names=['iranian', 'iran'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'royal_names': True,
                    'poetic_names': True
                }
            ),
            'turkish': EthnicityInfo(
                ethnicity='Turkish',
                primary_country='Turkey',
                region='Middle East',
                culture='Turkish',
                language='Turkish',
                alternative_names=['turkey'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'ottoman_influence': True
                }
            ),
            
            # European
            'italian': EthnicityInfo(
                ethnicity='Italian',
                primary_country='Italy',
                region='Europe',
                culture='Italian',
                language='Italian',
                alternative_names=['italy'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'regional_variations': True,
                    'saint_names': True
                }
            ),
            'french': EthnicityInfo(
                ethnicity='French',
                primary_country='France',
                region='Europe',
                culture='French',
                language='French',
                alternative_names=['france'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'regional_variations': True,
                    'aristocratic_names': True
                }
            ),
            'spanish': EthnicityInfo(
                ethnicity='Spanish',
                primary_country='Spain',
                region='Europe',
                culture='Spanish',
                language='Spanish',
                alternative_names=['spain'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_multiple_middle_names': True,
                    'maternal_paternal_surnames': True
                }
            ),
            'russian': EthnicityInfo(
                ethnicity='Russian',
                primary_country='Russia',
                region='Eastern Europe',
                culture='Eastern European',
                language='Russian',
                alternative_names=['russia'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'patronymic_system': True
                }
            ),
            'polish': EthnicityInfo(
                ethnicity='Polish',
                primary_country='Poland',
                region='Eastern Europe',
                culture='Eastern European',
                language='Polish',
                alternative_names=['poland'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'patronymic_system': True
                }
            ),
            'swedish': EthnicityInfo(
                ethnicity='Swedish',
                primary_country='Sweden',
                region='Scandinavia',
                culture='Scandinavian',
                language='Swedish',
                alternative_names=['sweden'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'patronymic_system': True,
                    'nature_names': True
                }
            ),
            'german': EthnicityInfo(
                ethnicity='German',
                primary_country='Germany',
                region='Central Europe',
                culture='German',
                language='German',
                alternative_names=['germany', 'deutsch'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'regional_variations': True,
                    'compound_names': True
                }
            ),
            
            # African
            'african_american': EthnicityInfo(
                ethnicity='African American',
                primary_country='United States',
                region='North America',
                culture='African American',
                language='English',
                alternative_names=['black_american'],
                diaspora_patterns=['traditional', 'cultural_revival', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'modern_african_american_names': True,
                    'cultural_revival': True
                }
            ),
            'nigerian': EthnicityInfo(
                ethnicity='Nigerian',
                primary_country='Nigeria',
                region='Africa',
                culture='African',
                language='English',
                alternative_names=['nigeria'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_middle_names': True,
                    'tribal_names': True
                }
            ),
            
            # American
            'american': EthnicityInfo(
                ethnicity='American',
                primary_country='United States',
                region='North America',
                culture='American',
                language='English',
                alternative_names=['united states', 'usa'],
                diaspora_patterns=['traditional', 'assimilated'],
                naming_conventions={
                    'uses_single_middle_name': True,
                    'various_ethnic_patterns': True,
                    'flexible_naming': True
                }
            )
        }
