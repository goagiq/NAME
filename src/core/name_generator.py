"""
Name Generator Service
Generates names using AI models and hybrid approach based on culture, locality, and religion.
"""

import logging
from typing import List, Dict, Any, Optional
import random
from datetime import datetime

from .models import IdentityRequest

logger = logging.getLogger(__name__)


class NameGenerator:
    """Service for generating culturally appropriate names."""
    
    def __init__(self):
        self.cultural_name_databases = self._initialize_cultural_databases()
        self.ai_model_available = False  # Will be set when AI is available
        
    def generate_names(self, request: IdentityRequest, 
                      cultural_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate multiple name candidates based on cultural context.
        
        Args:
            request: Identity request parameters
            cultural_context: Cultural context from locality agent
            
        Returns:
            List of name candidates with first_name, middle_name, last_name
        """
        logger.info(f"Generating names for {request.sex}, {request.location}, "
                   f"{request.race}, {request.religion}")
        
        # Use hybrid approach: rule-based + AI enhancement
        name_candidates = []
        used_first_names = set()
        used_last_names = set()
        
        # Generate 5 candidates with unique names
        max_attempts = 20  # Prevent infinite loops
        attempts = 0
        
        while len(name_candidates) < 5 and attempts < max_attempts:
            candidate = self._generate_single_name(
                request, cultural_context, used_first_names, used_last_names
            )
            if candidate:
                name_candidates.append(candidate)
                used_first_names.add(candidate['first_name'])
                used_last_names.add(candidate['last_name'])
            attempts += 1
        
        logger.info(f"Generated {len(name_candidates)} unique name candidates")
        return name_candidates
    


    def _generate_single_name(self, request: IdentityRequest, 
                            cultural_context: Dict[str, Any],
                            used_first_names: set = None,
                            used_last_names: set = None) -> Optional[Dict[str, Any]]:
        """Generate a single name candidate."""
        try:
            culture = cultural_context.get('culture', '').lower()
            race = request.race.lower()
            
            # Use culture-specific generation with fallback to race-based
            if culture == 'spanish':
                result = self._generate_spanish_name(request, cultural_context)
            elif culture == 'chinese':
                result = self._generate_chinese_name(request, cultural_context)
            elif culture == 'cambodian' or race in ['cambodian', 'khmer']:
                result = self._generate_cambodian_name(request, cultural_context)
            elif culture == 'indian' and cultural_context.get('regional_context'):
                result = self._generate_regional_indian_name(request, cultural_context)
            elif culture == 'thai' or race in ['thai', 'thailand']:
                result = self._generate_thai_name(request, cultural_context)
            elif culture == 'vietnamese' or race in ['vietnamese', 'vietnam']:
                result = self._generate_vietnamese_name(request, cultural_context)
            elif culture == 'korean' or race in ['korean', 'korea']:
                result = self._generate_korean_name(request, cultural_context)
            elif culture == 'japanese' or race in ['japanese', 'japan']:
                result = self._generate_japanese_name(request, cultural_context)
            elif culture == 'filipino' or race in ['filipino', 'philippines']:
                result = self._generate_filipino_name(request, cultural_context)
            elif culture == 'indian' or race in ['indian', 'india']:
                result = self._generate_indian_name(request, cultural_context)
            elif culture == 'arabic' or race in ['arabic', 'middle_eastern']:
                result = self._generate_arabic_name(request, cultural_context)
            elif culture == 'persian' or race in ['persian', 'iranian']:
                result = self._generate_persian_name(request, cultural_context)
            elif culture == 'turkish' or race in ['turkish', 'turkey']:
                result = self._generate_turkish_name(request, cultural_context)
            elif culture == 'african american' or race in ['african_american']:
                result = self._generate_african_american_name(request, cultural_context)
            elif culture == 'african' or race in ['african', 'nigerian']:
                result = self._generate_african_name(request, cultural_context)
            elif culture == 'eastern european' or race in ['russian', 'polish']:
                result = self._generate_eastern_european_name(request, cultural_context)
            elif culture == 'scandinavian' or race in ['swedish', 'norwegian']:
                result = self._generate_scandinavian_name(request, cultural_context)
            elif culture == 'italian' or race in ['italian', 'italy']:
                result = self._generate_italian_name(request, cultural_context)
            elif culture == 'french' or race in ['french', 'france']:
                result = self._generate_french_name(request, cultural_context)
            elif culture == 'american' or race in ['american']:
                result = self._generate_american_name(request, cultural_context)
            else:
                result = self._generate_generic_name(request, cultural_context)
            
            # Check for uniqueness if parameters are provided
            if result and used_first_names is not None and used_last_names is not None:
                first_name = result.get('first_name', '')
                last_name = result.get('last_name', '')
                
                # If name is already used, return None to indicate retry needed
                if first_name in used_first_names or last_name in used_last_names:
                    return None
            
            return result
                
        except Exception as e:
            logger.error(f"Name generation failed: {e}")
            return None
    
    def _generate_spanish_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Spanish-style name."""
        # Spanish names: First + Middle + Paternal Surname + Maternal Surname
        
        first_names = self._get_spanish_first_names(request.sex, request.birth_year)
        middle_names = self._get_spanish_middle_names(request.sex)
        paternal_surnames = self._get_spanish_paternal_surnames()
        maternal_surnames = self._get_spanish_maternal_surnames()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        paternal_surname = random.choice(paternal_surnames)
        maternal_surname = random.choice(maternal_surnames)
        
        # Combine surnames
        last_name = f"{paternal_surname} {maternal_surname}"
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Spanish naming convention with paternal and maternal surnames'
        }
    
    def _generate_chinese_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Chinese-style name."""
        # Check if this is a Taiwanese regional variant
        sub_region = cultural_context.get('sub_region', '').lower()
        naming_conventions = cultural_context.get('naming_conventions', {})
        
        if sub_region == 'taiwan' or 'taiwanese_names' in naming_conventions:
            # Use Taiwanese-specific names
            surnames = naming_conventions.get('taiwanese_surnames', self._get_chinese_surnames())
            given_names = naming_conventions.get('taiwanese_names', self._get_chinese_given_names(request.sex))
            
            surname = random.choice(surnames)
            given_name = random.choice(given_names)
            
            return {
                'first_name': given_name,  # Given name
                'middle_name': None,  # Taiwanese names typically don't have middle names
                'last_name': surname,  # Surname comes first in Chinese/Taiwanese
                'cultural_notes': 'Taiwanese naming convention with traditional Chinese names'
            }
        else:
            # Standard Chinese names
            surnames = self._get_chinese_surnames()
            given_names = self._get_chinese_given_names(request.sex)
            
            surname = random.choice(surnames)
            given_name = random.choice(given_names)
            
            return {
                'first_name': given_name,  # Given name
                'middle_name': None,  # Chinese names typically don't have middle names
                'last_name': surname,  # Surname comes first in Chinese
                'cultural_notes': 'Chinese naming convention with surname first'
            }
    

    
    def _generate_cambodian_name(self, request: IdentityRequest, 
                                cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Cambodian-style name."""
        # Cambodian names: First + Last (no middle names typically)
        
        first_names = self._get_cambodian_first_names(request.sex)
        last_names = self._get_cambodian_last_names()
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': None,  # Cambodian names typically don't have middle names
            'last_name': last_name,
            'cultural_notes': 'Cambodian naming convention with traditional Khmer names'
        }
    
    def _generate_thai_name(self, request: IdentityRequest, 
                           cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Thai-style name."""
        # Thai names: First + Last (no middle names typically)
        
        first_names = self._get_thai_first_names(request.sex)
        last_names = self._get_thai_last_names()
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': None,  # Thai names typically don't have middle names
            'last_name': last_name,
            'cultural_notes': 'Thai naming convention with traditional Thai names'
        }
    
    def _generate_vietnamese_name(self, request: IdentityRequest, 
                                 cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Vietnamese-style name."""
        # Vietnamese names: Last + First (surname first, no middle names typically)
        
        first_names = self._get_vietnamese_first_names(request.sex)
        last_names = self._get_vietnamese_last_names()
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': None,  # Vietnamese names typically don't have middle names
            'last_name': last_name,
            'cultural_notes': 'Vietnamese naming convention with surname first'
        }
    
    def _generate_american_name(self, request: IdentityRequest, 
                              cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate American-style name."""
        # American names: First + Middle + Last
        
        first_names = self._get_american_first_names(request.sex, request.birth_year, request.race)
        middle_names = self._get_american_middle_names(request.sex) if cultural_context.get('supports_middle_names') else [None]
        last_names = self._get_american_last_names(request.race)
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'American naming convention with ethnic considerations'
        }
    


    def _generate_generic_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate generic name when culture is not specifically handled."""
        
        first_names = self._get_generic_first_names(request.sex, request.birth_year)
        middle_names = self._get_generic_middle_names() if cultural_context.get('supports_middle_names') else [None]
        last_names = self._get_generic_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Generic naming convention'
        }
    
    def _get_spanish_first_names(self, sex: str, birth_year: int) -> List[str]:
        """Get Spanish first names based on sex and birth year."""
        if sex.lower() == 'male':
            return ['Carlos', 'Miguel', 'Javier', 'Antonio', 'Francisco', 'Luis', 'Jose', 'Manuel', 'David', 'Daniel']
        elif sex.lower() == 'female':
            return ['Maria', 'Carmen', 'Ana', 'Isabel', 'Rosa', 'Teresa', 'Elena', 'Sofia', 'Laura', 'Patricia']
        else:
            return ['Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn', 'Avery', 'Drew']
    
    def _get_spanish_middle_names(self, sex: str) -> List[str]:
        """Get Spanish middle names."""
        if sex.lower() == 'male':
            return ['Jose', 'Antonio', 'Luis', 'Miguel', 'Carlos', 'Francisco', 'Manuel', 'David', 'Javier', 'Daniel']
        elif sex.lower() == 'female':
            return ['Carmen', 'Ana', 'Isabel', 'Rosa', 'Teresa', 'Elena', 'Sofia', 'Laura', 'Patricia', 'Maria']
        else:
            return ['Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn', 'Avery', 'Drew']
    
    def _get_spanish_paternal_surnames(self) -> List[str]:
        """Get Spanish paternal surnames."""
        return ['Garcia', 'Rodriguez', 'Gonzalez', 'Fernandez', 'Lopez', 'Martinez', 'Sanchez', 'Perez', 'Gomez', 'Martin']
    
    def _get_spanish_maternal_surnames(self) -> List[str]:
        """Get Spanish maternal surnames."""
        return ['Hernandez', 'Jimenez', 'Diaz', 'Moreno', 'Muñoz', 'Alvarez', 'Romero', 'Alonso', 'Gutierrez', 'Navarro']
    
    def _get_chinese_surnames(self) -> List[str]:
        """Get Chinese surnames."""
        return ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou', 'Sun', 'Ma', 'Zhu', 'Hu', 'Guo']
    
    def _get_chinese_given_names(self, sex: str) -> List[str]:
        """Get Chinese given names."""
        if sex.lower() == 'male':
            return ['Wei', 'Ming', 'Jian', 'Hao', 'Lei', 'Feng', 'Tao', 'Jun', 'Bin', 'Yong']
        elif sex.lower() == 'female':
            return ['Mei', 'Ling', 'Hui', 'Xia', 'Yan', 'Fang', 'Hong', 'Jing', 'Ying', 'Li']
        else:
            return ['Wei', 'Ming', 'Mei', 'Ling', 'Hui', 'Xia', 'Yan', 'Fang', 'Hong', 'Jing']
    
    def _get_cambodian_first_names(self, sex: str) -> List[str]:
        """Get Cambodian first names."""
        if sex.lower() == 'male':
            return [
                'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey', 
                'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sopheak', 'Sokha', 'Rithy', 'Sambath', 
                'Sophearith', 'Sokun', 'Sopheakdey', 'Sokheng', 'Sopheakpanha', 'Sokunthea',
                'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey',
                'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea', 'Sopheak', 'Sokha', 'Rithy',
                'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey', 'Sokheng', 'Sopheakpanha',
                'Sokunthea', 'Sophea', 'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith',
                'Sokun', 'Sopheakdey', 'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea'
            ]
        elif sex.lower() == 'female':
            return [
                'Sophea', 'Sokunthea', 'Sopheakdey', 'Sokheng', 'Sopheakpanha', 'Sokun', 
                'Sophearith', 'Sambath', 'Rithy', 'Sokha', 'Sophea', 'Sokunthea', 'Sopheakdey',
                'Sokheng', 'Sopheakpanha', 'Sokun', 'Sophearith', 'Sambath', 'Rithy', 'Sokha',
                'Sophea', 'Sokunthea', 'Sopheakdey', 'Sokheng', 'Sopheakpanha', 'Sokun',
                'Sophearith', 'Sambath', 'Rithy', 'Sokha', 'Sophea', 'Sokunthea', 'Sopheakdey',
                'Sokheng', 'Sopheakpanha', 'Sokun', 'Sophearith', 'Sambath', 'Rithy', 'Sokha'
            ]
        else:
            return [
                'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey',
                'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea', 'Sopheak', 'Sokha', 'Rithy',
                'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey', 'Sokheng', 'Sopheakpanha',
                'Sokunthea', 'Sophea', 'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith',
                'Sokun', 'Sopheakdey', 'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea'
            ]
    
    def _get_cambodian_last_names(self) -> List[str]:
        """Get Cambodian last names."""
        return [
            'Sok', 'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey',
            'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea', 'Sokunthea', 'Sopheakdey', 'Sokheng',
            'Sok', 'Sopheak', 'Sokha', 'Rithy', 'Sambath', 'Sophearith', 'Sokun', 'Sopheakdey',
            'Sokheng', 'Sopheakpanha', 'Sokunthea', 'Sophea', 'Sokunthea', 'Sopheakdey', 'Sokheng'
        ]
    
    def _get_thai_first_names(self, sex: str) -> List[str]:
        """Get Thai first names."""
        if sex.lower() == 'male':
            return ['Somchai', 'Somsak', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong']
        elif sex.lower() == 'female':
            return ['Somjai', 'Somsri', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong']
        else:
            return ['Somchai', 'Somsak', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong']
    
    def _get_thai_last_names(self) -> List[str]:
        """Get Thai last names."""
        return ['Somsri', 'Somjai', 'Somchai', 'Somsak', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong', 'Somdet', 'Somkiat', 'Somphong']
    
    def _get_vietnamese_first_names(self, sex: str) -> List[str]:
        """Get Vietnamese first names."""
        if sex.lower() == 'male':
            return ['Minh', 'Duc', 'Huy', 'Tuan', 'Nam', 'Hoang', 'Phuoc', 'Khang', 'Bao', 'Khanh']
        elif sex.lower() == 'female':
            return ['Mai', 'Lan', 'Hoa', 'Thuy', 'Nga', 'Hong', 'Phuong', 'Huong', 'Trang', 'Linh']
        else:
            return ['Minh', 'Duc', 'Huy', 'Tuan', 'Nam', 'Hoang', 'Phuoc', 'Khang', 'Bao', 'Khanh']
    
    def _get_vietnamese_last_names(self) -> List[str]:
        """Get Vietnamese last names."""
        return ['Nguyen', 'Tran', 'Le', 'Pham', 'Hoang', 'Huynh', 'Phan', 'Vu', 'Vo', 'Dang', 'Bui', 'Do', 'Ho', 'Ngo', 'Duong']
    
    # Korean Name Generation Methods
    def _generate_korean_name(self, request: IdentityRequest, 
                            cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Korean-style name."""
        first_names = self._get_korean_first_names(request.sex)
        last_names = self._get_korean_last_names()
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': None,
            'last_name': last_name,
            'cultural_notes': 'Korean naming convention with surname first'
        }
    
    def _get_korean_first_names(self, sex: str) -> List[str]:
        """Get Korean first names."""
        if sex.lower() == 'male':
            return ['Min-jun', 'Seo-jun', 'Do-yoon', 'Ji-hun', 'Min-seok', 'Jun-seo', 'Dong-hyun', 'Jae-hyun', 'Min-ki', 'Seung-woo']
        elif sex.lower() == 'female':
            return ['Seo-yeon', 'Ji-yeon', 'Min-seo', 'Ye-eun', 'Ji-woo', 'Seo-hyun', 'Min-ji', 'Ye-jin', 'Ji-min', 'Seo-jin']
        else:
            return ['Min-jun', 'Seo-jun', 'Do-yoon', 'Ji-hun', 'Min-seok', 'Jun-seo', 'Dong-hyun', 'Jae-hyun', 'Min-ki', 'Seung-woo']
    
    def _get_korean_last_names(self) -> List[str]:
        """Get Korean last names."""
        return ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang', 'Lim', 'Han', 'Shin', 'Song', 'Ahn', 'Kwon']
    
    # Japanese Name Generation Methods
    def _generate_japanese_name(self, request: IdentityRequest, 
                              cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Japanese-style name."""
        first_names = self._get_japanese_first_names(request.sex)
        last_names = self._get_japanese_last_names()
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': None,
            'last_name': last_name,
            'cultural_notes': 'Japanese naming convention with surname first'
        }
    
    def _get_japanese_first_names(self, sex: str) -> List[str]:
        """Get Japanese first names."""
        if sex.lower() == 'male':
            return ['Hiroto', 'Yuto', 'Haruto', 'Sota', 'Yuki', 'Kento', 'Riku', 'Yamato', 'Takumi', 'Kenji']
        elif sex.lower() == 'female':
            return ['Yui', 'Aoi', 'Sakura', 'Hina', 'Yuka', 'Mai', 'Riko', 'Ami', 'Ema', 'Yuna']
        else:
            return ['Hiroto', 'Yuto', 'Haruto', 'Sota', 'Yuki', 'Kento', 'Riku', 'Yamato', 'Takumi', 'Kenji']
    
    def _get_japanese_last_names(self) -> List[str]:
        """Get Japanese last names."""
        return ['Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato', 'Yoshida', 'Yamada', 'Sasaki', 'Yamaguchi', 'Saito']
    
    # Filipino Name Generation Methods
    def _generate_filipino_name(self, request: IdentityRequest, 
                              cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Filipino-style name."""
        first_names = self._get_filipino_first_names(request.sex)
        middle_names = self._get_filipino_middle_names(request.sex)
        last_names = self._get_filipino_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Filipino naming convention with Spanish influence'
        }
    
    def _get_filipino_first_names(self, sex: str) -> List[str]:
        """Get Filipino first names."""
        if sex.lower() == 'male':
            return ['Jose', 'Antonio', 'Manuel', 'Francisco', 'Carlos', 'Miguel', 'Luis', 'Javier', 'David', 'Daniel']
        elif sex.lower() == 'female':
            return ['Maria', 'Ana', 'Carmen', 'Isabel', 'Rosa', 'Teresa', 'Elena', 'Sofia', 'Laura', 'Patricia']
        else:
            return ['Jose', 'Antonio', 'Manuel', 'Francisco', 'Carlos', 'Miguel', 'Luis', 'Javier', 'David', 'Daniel']
    
    def _get_filipino_middle_names(self, sex: str) -> List[str]:
        """Get Filipino middle names."""
        if sex.lower() == 'male':
            return ['Jose', 'Antonio', 'Luis', 'Miguel', 'Carlos', 'Francisco', 'Manuel', 'David', 'Javier', 'Daniel']
        elif sex.lower() == 'female':
            return ['Carmen', 'Ana', 'Isabel', 'Rosa', 'Teresa', 'Elena', 'Sofia', 'Laura', 'Patricia', 'Maria']
        else:
            return ['Jose', 'Antonio', 'Luis', 'Miguel', 'Carlos', 'Francisco', 'Manuel', 'David', 'Javier', 'Daniel']
    
    def _get_filipino_last_names(self) -> List[str]:
        """Get Filipino last names."""
        return ['Santos', 'Reyes', 'Cruz', 'Bautista', 'Ocampo', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Morales', 'Ramos', 'Gonzales', 'Perez', 'Lopez']
    
    # Indian Name Generation Methods
    def _generate_indian_name(self, request: IdentityRequest, 
                            cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Indian-style name."""
        first_names = self._get_indian_first_names(request.sex, request.religion)
        middle_names = self._get_indian_middle_names(request.sex)
        last_names = self._get_indian_last_names(request.religion)
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': f'Indian naming convention with {request.religion} influence'
        }
    
    def _get_indian_first_names(self, sex: str, religion: str) -> List[str]:
        """Get Indian first names based on religion."""
        if sex.lower() == 'male':
            if religion.lower() == 'hindu':
                return ['Arjun', 'Vikram', 'Rahul', 'Priya', 'Amit', 'Raj', 'Suresh', 'Kumar', 'Anand', 'Vishal']
            elif religion.lower() == 'muslim':
                return ['Ahmed', 'Ali', 'Hassan', 'Hussein', 'Mohammed', 'Omar', 'Yusuf', 'Zain', 'Ibrahim', 'Khalil']
            elif religion.lower() == 'sikh':
                return ['Gurpreet', 'Harpreet', 'Jaspreet', 'Manpreet', 'Simran', 'Kiran', 'Amar', 'Baljit', 'Daljit', 'Gurjit']
            else:
                return ['Arjun', 'Vikram', 'Rahul', 'Priya', 'Amit', 'Raj', 'Suresh', 'Kumar', 'Anand', 'Vishal']
        elif sex.lower() == 'female':
            if religion.lower() == 'hindu':
                return ['Priya', 'Anjali', 'Meera', 'Kavita', 'Sunita', 'Rekha', 'Lakshmi', 'Sita', 'Radha', 'Gita']
            elif religion.lower() == 'muslim':
                return ['Fatima', 'Aisha', 'Zara', 'Noor', 'Hana', 'Layla', 'Mariam', 'Yasmin', 'Amira', 'Nadia']
            elif religion.lower() == 'sikh':
                return ['Simran', 'Kiran', 'Harpreet', 'Gurpreet', 'Jaspreet', 'Manpreet', 'Baljit', 'Daljit', 'Gurjit', 'Amar']
            else:
                return ['Priya', 'Anjali', 'Meera', 'Kavita', 'Sunita', 'Rekha', 'Lakshmi', 'Sita', 'Radha', 'Gita']
        else:
            return ['Arjun', 'Vikram', 'Rahul', 'Priya', 'Amit', 'Raj', 'Suresh', 'Kumar', 'Anand', 'Vishal']
    
    def _get_indian_middle_names(self, sex: str) -> List[str]:
        """Get Indian middle names."""
        if sex.lower() == 'male':
            return ['Kumar', 'Singh', 'Patel', 'Sharma', 'Verma', 'Gupta', 'Malhotra', 'Kapoor', 'Chopra', 'Reddy']
        elif sex.lower() == 'female':
            return ['Devi', 'Kaur', 'Patel', 'Sharma', 'Verma', 'Gupta', 'Malhotra', 'Kapoor', 'Chopra', 'Reddy']
        else:
            return ['Kumar', 'Singh', 'Patel', 'Sharma', 'Verma', 'Gupta', 'Malhotra', 'Kapoor', 'Chopra', 'Reddy']
    
    def _get_indian_last_names(self, religion: str) -> List[str]:
        """Get Indian last names based on religion."""
        if religion.lower() == 'hindu':
            return ['Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Malhotra', 'Kapoor', 'Chopra', 'Reddy', 'Iyer', 'Menon', 'Nair', 'Pillai', 'Krishna']
        elif religion.lower() == 'muslim':
            return ['Khan', 'Ahmed', 'Ali', 'Hassan', 'Hussein', 'Mohammed', 'Omar', 'Yusuf', 'Zain', 'Ibrahim', 'Khalil', 'Rahman', 'Malik', 'Hussain', 'Qureshi']
        elif religion.lower() == 'sikh':
            return ['Singh', 'Kaur', 'Gill', 'Mann', 'Dhillon', 'Brar', 'Sidhu', 'Grewal', 'Randhawa', 'Cheema', 'Bhatti', 'Sandhu', 'Kang', 'Aulakh', 'Bains']
        else:
            return ['Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Malhotra', 'Kapoor', 'Chopra', 'Reddy']
    
    # Arabic Name Generation Methods
    def _generate_arabic_name(self, request: IdentityRequest, 
                            cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Arabic-style name."""
        first_names = self._get_arabic_first_names(request.sex)
        middle_names = self._get_arabic_middle_names(request.sex)
        last_names = self._get_arabic_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Arabic naming convention with patronymic system'
        }
    
    def _get_arabic_first_names(self, sex: str) -> List[str]:
        """Get Arabic first names."""
        if sex.lower() == 'male':
            return ['Ahmed', 'Ali', 'Hassan', 'Hussein', 'Mohammed', 'Omar', 'Yusuf', 'Zain', 'Ibrahim', 'Khalil', 'Mahmoud', 'Mustafa', 'Rashid', 'Tariq', 'Waleed']
        elif sex.lower() == 'female':
            return ['Fatima', 'Aisha', 'Zara', 'Noor', 'Hana', 'Layla', 'Mariam', 'Yasmin', 'Amira', 'Nadia', 'Sara', 'Leila', 'Rania', 'Dalia', 'Samira']
        else:
            return ['Ahmed', 'Ali', 'Hassan', 'Hussein', 'Mohammed', 'Omar', 'Yusuf', 'Zain', 'Ibrahim', 'Khalil']
    
    def _get_arabic_middle_names(self, sex: str) -> List[str]:
        """Get Arabic middle names."""
        if sex.lower() == 'male':
            return ['Abdullah', 'Hassan', 'Hussein', 'Ibrahim', 'Khalil', 'Mahmoud', 'Mustafa', 'Rashid', 'Tariq', 'Waleed']
        elif sex.lower() == 'female':
            return ['Fatima', 'Aisha', 'Zara', 'Noor', 'Hana', 'Layla', 'Mariam', 'Yasmin', 'Amira', 'Nadia']
        else:
            return ['Abdullah', 'Hassan', 'Hussein', 'Ibrahim', 'Khalil', 'Mahmoud', 'Mustafa', 'Rashid', 'Tariq', 'Waleed']
    
    def _get_arabic_last_names(self) -> List[str]:
        """Get Arabic last names."""
        return ['Al-Rashid', 'Al-Zahra', 'Al-Mahmoud', 'Al-Hassan', 'Al-Hussein', 'Al-Ibrahim', 'Al-Khalil', 'Al-Mustafa', 'Al-Tariq', 'Al-Waleed', 'Al-Fatima', 'Al-Aisha', 'Al-Zara', 'Al-Noor', 'Al-Hana']
    
    # Persian Name Generation Methods
    def _generate_persian_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Persian-style name."""
        first_names = self._get_persian_first_names(request.sex)
        middle_names = self._get_persian_middle_names(request.sex)
        last_names = self._get_persian_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Persian naming convention with poetic and royal influences'
        }
    
    def _get_persian_first_names(self, sex: str) -> List[str]:
        """Get Persian first names."""
        if sex.lower() == 'male':
            return ['Arash', 'Darius', 'Cyrus', 'Kaveh', 'Rostam', 'Sohrab', 'Bahram', 'Farhad', 'Khosrow', 'Shahriar', 'Amir', 'Reza', 'Ali', 'Hassan', 'Hussein']
        elif sex.lower() == 'female':
            return ['Shirin', 'Roxana', 'Yasmin', 'Parisa', 'Azadeh', 'Mina', 'Neda', 'Sara', 'Leila', 'Roya', 'Fatima', 'Aisha', 'Zara', 'Noor', 'Hana']
        else:
            return ['Arash', 'Darius', 'Cyrus', 'Kaveh', 'Rostam', 'Sohrab', 'Bahram', 'Farhad', 'Khosrow', 'Shahriar']
    
    def _get_persian_middle_names(self, sex: str) -> List[str]:
        """Get Persian middle names."""
        if sex.lower() == 'male':
            return ['Arash', 'Darius', 'Cyrus', 'Kaveh', 'Rostam', 'Sohrab', 'Bahram', 'Farhad', 'Khosrow', 'Shahriar']
        elif sex.lower() == 'female':
            return ['Shirin', 'Roxana', 'Yasmin', 'Parisa', 'Azadeh', 'Mina', 'Neda', 'Sara', 'Leila', 'Roya']
        else:
            return ['Arash', 'Darius', 'Cyrus', 'Kaveh', 'Rostam', 'Sohrab', 'Bahram', 'Farhad', 'Khosrow', 'Shahriar']
    
    def _get_persian_last_names(self) -> List[str]:
        """Get Persian last names."""
        return ['Ahmadi', 'Hassani', 'Hussein', 'Ibrahimi', 'Khalili', 'Mahmoudi', 'Mustafavi', 'Rashidi', 'Tariqi', 'Waleedi', 'Fatimi', 'Aishai', 'Zarai', 'Noori', 'Hanai']
    
    # Turkish Name Generation Methods
    def _generate_turkish_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Turkish-style name."""
        first_names = self._get_turkish_first_names(request.sex)
        middle_names = self._get_turkish_middle_names(request.sex)
        last_names = self._get_turkish_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Turkish naming convention with Ottoman influence'
        }
    
    def _get_turkish_first_names(self, sex: str) -> List[str]:
        """Get Turkish first names."""
        if sex.lower() == 'male':
            return ['Mehmet', 'Mustafa', 'Ahmet', 'Ali', 'Hasan', 'Hussein', 'Ibrahim', 'Kemal', 'Orhan', 'Osman', 'Selim', 'Suleyman', 'Tarik', 'Yusuf', 'Ziya']
        elif sex.lower() == 'female':
            return ['Ayse', 'Fatma', 'Zeynep', 'Emine', 'Hatice', 'Meryem', 'Elif', 'Esra', 'Selin', 'Deniz', 'Gizem', 'Merve', 'Seda', 'Yasmin', 'Nur']
        else:
            return ['Mehmet', 'Mustafa', 'Ahmet', 'Ali', 'Hasan', 'Hussein', 'Ibrahim', 'Kemal', 'Orhan', 'Osman']
    
    def _get_turkish_middle_names(self, sex: str) -> List[str]:
        """Get Turkish middle names."""
        if sex.lower() == 'male':
            return ['Mehmet', 'Mustafa', 'Ahmet', 'Ali', 'Hasan', 'Hussein', 'Ibrahim', 'Kemal', 'Orhan', 'Osman']
        elif sex.lower() == 'female':
            return ['Ayse', 'Fatma', 'Zeynep', 'Emine', 'Hatice', 'Meryem', 'Elif', 'Esra', 'Selin', 'Deniz']
        else:
            return ['Mehmet', 'Mustafa', 'Ahmet', 'Ali', 'Hasan', 'Hussein', 'Ibrahim', 'Kemal', 'Orhan', 'Osman']
    
    def _get_turkish_last_names(self) -> List[str]:
        """Get Turkish last names."""
        return ['Yilmaz', 'Kaya', 'Demir', 'Celik', 'Sahin', 'Yildiz', 'Yildirim', 'Ozdemir', 'Arslan', 'Dogan', 'Kilic', 'Aslan', 'Cetin', 'Erdogan', 'Gunes']
    
    # Italian Name Generation Methods
    def _generate_italian_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Italian-style name."""
        first_names = self._get_italian_first_names(request.sex)
        middle_names = self._get_italian_middle_names(request.sex)
        last_names = self._get_italian_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Italian naming convention with regional variations'
        }
    
    def _get_italian_first_names(self, sex: str) -> List[str]:
        """Get Italian first names."""
        if sex.lower() == 'male':
            return ['Marco', 'Giuseppe', 'Luca', 'Antonio', 'Giovanni', 'Roberto', 'Alessandro', 'Andrea', 'Matteo', 'Stefano', 'Paolo', 'Mario', 'Carlo', 'Franco', 'Vincenzo']
        elif sex.lower() == 'female':
            return ['Maria', 'Giulia', 'Sofia', 'Alessia', 'Chiara', 'Valentina', 'Martina', 'Elena', 'Laura', 'Anna', 'Francesca', 'Elisa', 'Silvia', 'Monica', 'Cristina']
        else:
            return ['Marco', 'Giuseppe', 'Luca', 'Antonio', 'Giovanni', 'Roberto', 'Alessandro', 'Andrea', 'Matteo', 'Stefano']
    
    def _get_italian_middle_names(self, sex: str) -> List[str]:
        """Get Italian middle names."""
        if sex.lower() == 'male':
            return ['Marco', 'Giuseppe', 'Luca', 'Antonio', 'Giovanni', 'Roberto', 'Alessandro', 'Andrea', 'Matteo', 'Stefano']
        elif sex.lower() == 'female':
            return ['Maria', 'Giulia', 'Sofia', 'Alessia', 'Chiara', 'Valentina', 'Martina', 'Elena', 'Laura', 'Anna']
        else:
            return ['Marco', 'Giuseppe', 'Luca', 'Antonio', 'Giovanni', 'Roberto', 'Alessandro', 'Andrea', 'Matteo', 'Stefano']
    
    def _get_italian_last_names(self) -> List[str]:
        """Get Italian last names."""
        return ['Rossi', 'Ferrari', 'Russo', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco', 'Bruno', 'Galli', 'Rinaldi', 'Fontana', 'Caruso', 'Ferrara']
    
    # French Name Generation Methods
    def _generate_french_name(self, request: IdentityRequest, 
                            cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate French-style name."""
        first_names = self._get_french_first_names(request.sex)
        middle_names = self._get_french_middle_names(request.sex)
        last_names = self._get_french_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'French naming convention with regional variations'
        }
    
    def _get_french_first_names(self, sex: str) -> List[str]:
        """Get French first names."""
        if sex.lower() == 'male':
            return ['Jean', 'Pierre', 'Michel', 'Andre', 'Philippe', 'Francois', 'Claude', 'Jacques', 'Bernard', 'Marcel', 'Henri', 'Louis', 'Paul', 'Robert', 'Daniel']
        elif sex.lower() == 'female':
            return ['Marie', 'Jeanne', 'Francoise', 'Monique', 'Nicole', 'Danielle', 'Christine', 'Sylvie', 'Martine', 'Catherine', 'Isabelle', 'Sophie', 'Anne', 'Claire', 'Elise']
        else:
            return ['Jean', 'Pierre', 'Michel', 'Andre', 'Philippe', 'Francois', 'Claude', 'Jacques', 'Bernard', 'Marcel']
    
    def _get_french_middle_names(self, sex: str) -> List[str]:
        """Get French middle names."""
        if sex.lower() == 'male':
            return ['Jean', 'Pierre', 'Michel', 'Andre', 'Philippe', 'Francois', 'Claude', 'Jacques', 'Bernard', 'Marcel']
        elif sex.lower() == 'female':
            return ['Marie', 'Jeanne', 'Francoise', 'Monique', 'Nicole', 'Danielle', 'Christine', 'Sylvie', 'Martine', 'Catherine']
        else:
            return ['Jean', 'Pierre', 'Michel', 'Andre', 'Philippe', 'Francois', 'Claude', 'Jacques', 'Bernard', 'Marcel']
    
    def _get_french_last_names(self) -> List[str]:
        """Get French last names."""
        return ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia']
    
    # Eastern European Name Generation Methods
    def _generate_eastern_european_name(self, request: IdentityRequest, 
                                      cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Eastern European-style name."""
        first_names = self._get_eastern_european_first_names(request.sex)
        middle_names = self._get_eastern_european_middle_names(request.sex)
        last_names = self._get_eastern_european_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Eastern European naming convention with patronymic system'
        }
    
    def _get_eastern_european_first_names(self, sex: str) -> List[str]:
        """Get Eastern European first names."""
        if sex.lower() == 'male':
            return ['Ivan', 'Dmitri', 'Sergei', 'Vladimir', 'Nikolai', 'Andrei', 'Mikhail', 'Alexei', 'Yuri', 'Boris', 'Piotr', 'Jan', 'Tomasz', 'Marek', 'Krzysztof']
        elif sex.lower() == 'female':
            return ['Anna', 'Maria', 'Elena', 'Natalia', 'Olga', 'Irina', 'Svetlana', 'Tatiana', 'Yulia', 'Ludmila', 'Katarzyna', 'Agnieszka', 'Malgorzata', 'Ewa', 'Barbara']
        else:
            return ['Ivan', 'Dmitri', 'Sergei', 'Vladimir', 'Nikolai', 'Andrei', 'Mikhail', 'Alexei', 'Yuri', 'Boris']
    
    def _get_eastern_european_middle_names(self, sex: str) -> List[str]:
        """Get Eastern European middle names."""
        if sex.lower() == 'male':
            return ['Ivanovich', 'Dmitrievich', 'Sergeevich', 'Vladimirovich', 'Nikolaevich', 'Andreevich', 'Mikhailovich', 'Alexeevich', 'Yurievich', 'Borisovich']
        elif sex.lower() == 'female':
            return ['Ivanovna', 'Dmitrievna', 'Sergeevna', 'Vladimirovna', 'Nikolaevna', 'Andreevna', 'Mikhailovna', 'Alexeevna', 'Yurievna', 'Borisovna']
        else:
            return ['Ivanovich', 'Dmitrievich', 'Sergeevich', 'Vladimirovich', 'Nikolaevich', 'Andreevich', 'Mikhailovich', 'Alexeevich', 'Yurievich', 'Borisovich']
    
    def _get_eastern_european_last_names(self) -> List[str]:
        """Get Eastern European last names."""
        return ['Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Vasiliev', 'Petrov', 'Sokolov', 'Mikhailov', 'Novikov', 'Fedorov', 'Kowalski', 'Nowak', 'Wisniewski', 'Wojcik', 'Kowalczyk']
    
    # Scandinavian Name Generation Methods
    def _generate_scandinavian_name(self, request: IdentityRequest, 
                                  cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Scandinavian-style name."""
        first_names = self._get_scandinavian_first_names(request.sex)
        middle_names = self._get_scandinavian_middle_names(request.sex)
        last_names = self._get_scandinavian_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'Scandinavian naming convention with patronymic system'
        }
    
    def _get_scandinavian_first_names(self, sex: str) -> List[str]:
        """Get Scandinavian first names."""
        if sex.lower() == 'male':
            return ['Erik', 'Lars', 'Anders', 'Johan', 'Per', 'Nils', 'Karl', 'Mikael', 'Bjorn', 'Gustav', 'Olav', 'Magnus', 'Sven', 'Henrik', 'Thomas']
        elif sex.lower() == 'female':
            return ['Anna', 'Maria', 'Karin', 'Eva', 'Birgitta', 'Kerstin', 'Elisabeth', 'Margareta', 'Ingrid', 'Kristina', 'Helena', 'Sofia', 'Emma', 'Ida', 'Astrid']
        else:
            return ['Erik', 'Lars', 'Anders', 'Johan', 'Per', 'Nils', 'Karl', 'Mikael', 'Bjorn', 'Gustav']
    
    def _get_scandinavian_middle_names(self, sex: str) -> List[str]:
        """Get Scandinavian middle names."""
        if sex.lower() == 'male':
            return ['Eriksson', 'Larsson', 'Andersson', 'Johansson', 'Persson', 'Nilsson', 'Karlsson', 'Mikaelsson', 'Bjornsson', 'Gustavsson']
        elif sex.lower() == 'female':
            return ['Eriksdotter', 'Larsdotter', 'Andersdotter', 'Johansdotter', 'Persdotter', 'Nilsdotter', 'Karlsdotter', 'Mikaelsdotter', 'Bjornsdotter', 'Gustavsdotter']
        else:
            return ['Eriksson', 'Larsson', 'Andersson', 'Johansson', 'Persson', 'Nilsson', 'Karlsson', 'Mikaelsson', 'Bjornsson', 'Gustavsson']
    
    def _get_scandinavian_last_names(self) -> List[str]:
        """Get Scandinavian last names."""
        return ['Andersson', 'Johansson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson', 'Pettersson', 'Jonsson', 'Jansson', 'Hansson', 'Bengtsson']
    
    # African Name Generation Methods
    def _generate_african_name(self, request: IdentityRequest, 
                             cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate African-style name."""
        first_names = self._get_african_first_names(request.sex)
        middle_names = self._get_african_middle_names(request.sex)
        last_names = self._get_african_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'African naming convention with tribal and colonial influences'
        }
    
    def _get_african_first_names(self, sex: str) -> List[str]:
        """Get African first names."""
        if sex.lower() == 'male':
            return ['Kofi', 'Kwame', 'Akwasi', 'Kwesi', 'Kobena', 'Kwaku', 'Yaw', 'Kwadwo', 'Kwabena', 'Kofi', 'Chukwudi', 'Chukwuma', 'Chukwuka', 'Chukwuebuka', 'Chukwunonso']
        elif sex.lower() == 'female':
            return ['Akosua', 'Adwoa', 'Abenaa', 'Akua', 'Yaa', 'Afua', 'Ama', 'Akosua', 'Adwoa', 'Abenaa', 'Ngozi', 'Chioma', 'Chidinma', 'Chiamaka', 'Chinwe']
        else:
            return ['Kofi', 'Kwame', 'Akwasi', 'Kwesi', 'Kobena', 'Kwaku', 'Yaw', 'Kwadwo', 'Kwabena', 'Kofi']
    
    def _get_african_middle_names(self, sex: str) -> List[str]:
        """Get African middle names."""
        if sex.lower() == 'male':
            return ['Kofi', 'Kwame', 'Akwasi', 'Kwesi', 'Kobena', 'Kwaku', 'Yaw', 'Kwadwo', 'Kwabena', 'Kofi']
        elif sex.lower() == 'female':
            return ['Akosua', 'Adwoa', 'Abenaa', 'Akua', 'Yaa', 'Afua', 'Ama', 'Akosua', 'Adwoa', 'Abenaa']
        else:
            return ['Kofi', 'Kwame', 'Akwasi', 'Kwesi', 'Kobena', 'Kwaku', 'Yaw', 'Kwadwo', 'Kwabena', 'Kofi']
    
    def _get_african_last_names(self) -> List[str]:
        """Get African last names."""
        return ['Mensah', 'Owusu', 'Osei', 'Kufuor', 'Akufo', 'Addo', 'Mensah', 'Owusu', 'Osei', 'Kufuor', 'Akufo', 'Addo', 'Mensah', 'Owusu', 'Osei']
    
    # African American Name Generation Methods
    def _generate_african_american_name(self, request: IdentityRequest, 
                                      cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate African American-style name."""
        first_names = self._get_african_american_first_names(request.sex)
        middle_names = self._get_african_american_middle_names(request.sex)
        last_names = self._get_african_american_last_names()
        
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names) if cultural_context.get('supports_middle_names') else None
        last_name = random.choice(last_names)
        
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'cultural_notes': 'African American naming convention with cultural revival'
        }
    
    def _get_african_american_first_names(self, sex: str) -> List[str]:
        """Get African American first names."""
        if sex.lower() == 'male':
            return ['DeAndre', 'Tyrone', 'Malik', 'Darnell', 'Terrell', 'Marquis', 'Darius', 'Xavier', 'Andre', 'Marcus', 'Darnell', 'Terrell', 'Marquis', 'Darius', 'Xavier']
        elif sex.lower() == 'female':
            return ['Shaniqua', 'Latoya', 'Keisha', 'Tamika', 'Ebony', 'Imani', 'Aaliyah', 'Destiny', 'Precious', 'Unique', 'Shaniqua', 'Latoya', 'Keisha', 'Tamika', 'Ebony']
        else:
            return ['DeAndre', 'Tyrone', 'Malik', 'Darnell', 'Terrell', 'Marquis', 'Darius', 'Xavier', 'Andre', 'Marcus']
    
    def _get_african_american_middle_names(self, sex: str) -> List[str]:
        """Get African American middle names."""
        if sex.lower() == 'male':
            return ['DeAndre', 'Tyrone', 'Malik', 'Darnell', 'Terrell', 'Marquis', 'Darius', 'Xavier', 'Andre', 'Marcus']
        elif sex.lower() == 'female':
            return ['Shaniqua', 'Latoya', 'Keisha', 'Tamika', 'Ebony', 'Imani', 'Aaliyah', 'Destiny', 'Precious', 'Unique']
        else:
            return ['DeAndre', 'Tyrone', 'Malik', 'Darnell', 'Terrell', 'Marquis', 'Darius', 'Xavier', 'Andre', 'Marcus']
    
    def _get_african_american_last_names(self) -> List[str]:
        """Get African American last names."""
        return ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia']
    
    def _get_american_first_names(self, sex: str, birth_year: int, race: str) -> List[str]:
        """Get American first names based on sex, birth year, and race."""
        # Popular names from 1980s-1990s for the birth year
        if sex.lower() == 'male':
            return ['Michael', 'Christopher', 'Matthew', 'Joshua', 'David', 'James', 'Daniel', 'Robert', 'John', 'Joseph']
        elif sex.lower() == 'female':
            return ['Jessica', 'Ashley', 'Amanda', 'Sarah', 'Stephanie', 'Nicole', 'Heather', 'Elizabeth', 'Megan', 'Lauren']
        else:
            return ['Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn', 'Avery', 'Drew']
    
    def _get_american_middle_names(self, sex: str) -> List[str]:
        """Get American middle names."""
        if sex.lower() == 'male':
            return ['James', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Christopher', 'Charles']
        elif sex.lower() == 'female':
            return ['Marie', 'Anne', 'Lynn', 'Elizabeth', 'Rose', 'Grace', 'Jane', 'Claire', 'Faith', 'Hope']
        else:
            return ['Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn', 'Avery', 'Drew']
    
    def _get_american_last_names(self, race: str) -> List[str]:
        """Get American last names based on race/ethnicity."""
        if race.lower() == 'african american':
            return ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez']
        elif race.lower() == 'hispanic':
            return ['Garcia', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Wilson', 'Anderson', 'Thomas']
        elif race.lower() == 'asian':
            return ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou']
        else:
            return ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    def _get_generic_first_names(self, sex: str, birth_year: int) -> List[str]:
        """Get generic first names."""
        if sex.lower() == 'male':
            return ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard', 'Joseph', 'Thomas', 'Christopher']
        elif sex.lower() == 'female':
            return ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        else:
            return ['Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn', 'Avery', 'Drew']
    
    def _get_generic_middle_names(self) -> List[str]:
        """Get generic middle names."""
        return ['Marie', 'Anne', 'Lynn', 'Elizabeth', 'Rose', 'Grace', 'Jane', 'Claire', 'Faith', 'Hope', None]
    
    def _get_generic_last_names(self) -> List[str]:
        """Get generic last names."""
        return ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    def _initialize_cultural_databases(self) -> Dict[str, Any]:
        """Initialize cultural name databases."""
        return {
            'spanish': {
                'first_names': {
                    'male': ['Carlos', 'Miguel', 'Javier', 'Antonio', 'Francisco'],
                    'female': ['Maria', 'Carmen', 'Ana', 'Isabel', 'Rosa']
                },
                'surnames': ['Garcia', 'Rodriguez', 'Gonzalez', 'Fernandez', 'Lopez']
            },
            'chinese': {
                'surnames': ['Wang', 'Li', 'Zhang', 'Liu', 'Chen'],
                'given_names': {
                    'male': ['Wei', 'Ming', 'Jian', 'Hao', 'Lei'],
                    'female': ['Mei', 'Ling', 'Hui', 'Xia', 'Yan']
                }
            },
            'american': {
                'first_names': {
                    'male': ['Michael', 'Christopher', 'Matthew', 'Joshua', 'David'],
                    'female': ['Jessica', 'Ashley', 'Amanda', 'Sarah', 'Stephanie']
                },
                'last_names': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
            }
        }

    def _generate_regional_indian_name(self, request: IdentityRequest, 
                                     cultural_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a regional Indian name based on sub-region context."""
        try:
            sub_region = cultural_context.get('sub_region', '').lower()
            naming_conventions = cultural_context.get('naming_conventions', {})
            
            # Get regional name preferences
            if 'south india' in sub_region or any(region in sub_region for region in ['tamil', 'telugu', 'malayalam', 'kannada']):
                # South Indian names
                if request.sex.lower() == 'female':
                    first_names = naming_conventions.get('south_indian_names', [
                        'Priya', 'Lakshmi', 'Meenakshi', 'Saraswati', 'Parvati', 'Gayatri',
                        'Anitha', 'Kavitha', 'Sunitha', 'Vijaya', 'Padma', 'Sita', 'Radha',
                        'Savitha', 'Rekha', 'Usha', 'Geetha', 'Leela', 'Maya', 'Rani',
                        'Swathi', 'Divya', 'Anjali', 'Deepa', 'Kavya', 'Nisha', 'Pooja'
                    ])
                else:
                    first_names = [
                        'Arun', 'Kumar', 'Raj', 'Suresh', 'Mohan', 'Ramesh', 'Prakash',
                        'Anand', 'Vijay', 'Srinivas', 'Venkat', 'Krishna', 'Ganesh',
                        'Shiva', 'Ravi', 'Murali', 'Sundar', 'Balaji', 'Narayan', 'Raghu'
                    ]
                
                surnames = naming_conventions.get('south_indian_surnames', [
                    'Iyer', 'Iyengar', 'Pillai', 'Chettiar', 'Mudaliar', 'Reddy', 'Naidu',
                    'Gounder', 'Thevar', 'Vanniyar', 'Kallar', 'Maravar', 'Aghamudayar',
                    'Nair', 'Menon', 'Kurup', 'Nambiar', 'Thampi', 'Unni', 'Panicker',
                    'Gowda', 'Hegde', 'Shetty', 'Pai', 'Bhat', 'Rao', 'Kumar'
                ])
                
            elif 'north india' in sub_region or any(region in sub_region for region in ['punjab', 'rajasthan', 'bihar', 'uttar pradesh']):
                # North Indian names
                if request.sex.lower() == 'female':
                    first_names = naming_conventions.get('north_indian_names', [
                        'Priya', 'Anjali', 'Meera', 'Kavita', 'Sunita', 'Rekha', 'Lakshmi',
                        'Sita', 'Radha', 'Gita', 'Neha', 'Pooja', 'Rashmi', 'Shanti', 'Uma'
                    ])
                else:
                    first_names = [
                        'Arjun', 'Vikram', 'Rahul', 'Amit', 'Raj', 'Suresh', 'Kumar',
                        'Anand', 'Vishal', 'Ravi', 'Mohan', 'Ramesh', 'Prakash', 'Anand'
                    ]
                
                surnames = naming_conventions.get('north_indian_surnames', [
                    'Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Malhotra',
                    'Kapoor', 'Chopra', 'Reddy', 'Khan', 'Ahmed', 'Ali', 'Hassan'
                ])
                
            else:
                # Generic Indian names (fallback)
                return self._generate_indian_name(request, cultural_context)
            
            # Generate name components
            first_name = random.choice(first_names)
            last_name = random.choice(surnames)
            
            # Indians may use middle names, but not always
            middle_name = None
            if random.random() < 0.3:  # 30% chance of middle name
                middle_names = [
                    'Devi', 'Lakshmi', 'Saraswati', 'Parvati', 'Gayatri', 'Anitha',
                    'Kavitha', 'Sunitha', 'Vijaya', 'Padma', 'Sita', 'Radha', 'Savitha'
                ]
                middle_name = random.choice(middle_names)
            
            name_data = {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'cultural_context': cultural_context
            }
            
            return name_data
            
        except Exception as e:
            logger.error(f"Error generating regional Indian name: {e}")
            return None
