"""
Watchlist Validation Service
Validates names against publicly available government and industry watchlists.
"""

import asyncio
import aiohttp
import json
import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import hashlib
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class WatchlistResult:
    """Result of a watchlist validation check."""
    name: str
    is_blocked: bool
    sources: List[str]
    confidence: float
    reasons: List[str]
    last_updated: datetime
    raw_data: Dict[str, Any]

@dataclass
class ValidationSource:
    """Configuration for a validation source."""
    name: str
    url: str
    api_key_required: bool
    rate_limit: int  # requests per minute
    enabled: bool = True
    api_key: Optional[str] = None

class WatchlistValidator:
    """Comprehensive watchlist validation service."""
    
    def __init__(self, db_path: str = "name_generation.db"):
        self.db_path = db_path
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache_duration_hours = 24
        
        # Initialize validation sources
        self.sources = self._initialize_sources()
        
        # Initialize database
        self._init_database()
        
        logger.info("WatchlistValidator initialized")
    
    def _initialize_sources(self) -> Dict[str, ValidationSource]:
        """Initialize validation sources with publicly available databases."""
        return {
            # Government Watchlists
            "ofac_sdn": ValidationSource(
                name="OFAC Specially Designated Nationals",
                url="https://api.trade.gov/consolidated_screening_list/search",
                api_key_required=True,
                rate_limit=60
            ),
            "fbi_wanted": ValidationSource(
                name="FBI Most Wanted",
                url="https://api.fbi.gov/wanted/v1/list",
                api_key_required=False,
                rate_limit=30
            ),
            "interpol_red": ValidationSource(
                name="Interpol Red Notices",
                url="https://ws-public.interpol.int/notices/v1/red",
                api_key_required=False,
                rate_limit=20
            ),
            "un_sanctions": ValidationSource(
                name="UN Sanctions List",
                url="https://scsanctions.un.org/resources/xml/en/consolidated.xml",
                api_key_required=False,
                rate_limit=10
            ),
            
            # Aviation Security
            "no_fly_list": ValidationSource(
                name="TSA No Fly List (Public Data)",
                url="https://www.tsa.gov/travel/security-screening/individuals",
                api_key_required=False,
                rate_limit=5
            ),
            
            # Financial Crime
            "finra_brokercheck": ValidationSource(
                name="FINRA BrokerCheck",
                url="https://api.finra.org/brokercheck/v1/search",
                api_key_required=True,
                rate_limit=30
            ),
            
            # Law Enforcement
            "national_sex_offender": ValidationSource(
                name="National Sex Offender Registry",
                url="https://www.nsopw.gov/api/search",
                api_key_required=False,
                rate_limit=10
            ),
            "dru_sjodin_nsopw": ValidationSource(
                name="Dru Sjodin National Sex Offender Public Website (NSOPW)",
                url="https://www.nsopw.gov/api/search",
                api_key_required=False,
                rate_limit=10
            ),
            "murder_accountability_project": ValidationSource(
                name="Murder Accountability Project (MAP)",
                url="https://www.murderdata.org/api/search",
                api_key_required=False,
                rate_limit=5
            ),
            "radford_serial_killer_db": ValidationSource(
                name="Radford/FGCU Serial Killer Database",
                url="https://www.radford.edu/content/csat/home/radford-serial-killer-database.html",
                api_key_required=False,
                rate_limit=5
            ),
            
            # International Databases
            "european_sanctions": ValidationSource(
                name="EU Sanctions List",
                url="https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList/content",
                api_key_required=False,
                rate_limit=5
            ),
            "uk_sanctions": ValidationSource(
                name="UK Sanctions List",
                url="https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/",
                api_key_required=False,
                rate_limit=5
            ),
            "canada_sanctions": ValidationSource(
                name="Canada Sanctions List",
                url="https://www.international.gc.ca/world-monde/international_relations-relations_internationales/sanctions/consolidated-consolide.aspx",
                api_key_required=False,
                rate_limit=5
            ),
            
            # Industry Watchlists
            "world_check": ValidationSource(
                name="World-Check (Thomson Reuters)",
                url="https://risk.lexisnexis.com/api/v1/worldcheck",
                api_key_required=True,
                rate_limit=100
            ),
            "dow_jones": ValidationSource(
                name="Dow Jones Risk & Compliance",
                url="https://api.dowjones.com/risk-compliance/v1/search",
                api_key_required=True,
                rate_limit=50
            ),
            
            # Public Records
            "public_records": ValidationSource(
                name="Public Records Search",
                url="https://api.publicrecords.com/search",
                api_key_required=True,
                rate_limit=20
            ),
            
            # Social Media Monitoring
            "social_media_monitoring": ValidationSource(
                name="Social Media Risk Assessment",
                url="https://api.socialmediarisk.com/check",
                api_key_required=True,
                rate_limit=30
            )
        }
    
    def _init_database(self):
        """Initialize database tables for caching validation results."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create validation cache table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS watchlist_cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_hash TEXT UNIQUE NOT NULL,
                        full_name TEXT NOT NULL,
                        is_blocked BOOLEAN NOT NULL,
                        sources TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        reasons TEXT NOT NULL,
                        raw_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL
                    )
                """)
                
                # Create validation sources table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS validation_sources (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_name TEXT UNIQUE NOT NULL,
                        last_check TIMESTAMP,
                        status TEXT DEFAULT 'active',
                        error_count INTEGER DEFAULT 0
                    )
                """)
                
                # Create validation logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS validation_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        source TEXT NOT NULL,
                        result TEXT NOT NULL,
                        response_time REAL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database tables initialized")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'NameGenerationSystem/1.0 (WatchlistValidator)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _normalize_name(self, name: str) -> str:
        """Normalize name for consistent comparison."""
        # Remove extra spaces and convert to lowercase
        normalized = re.sub(r'\s+', ' ', name.strip().lower())
        # Remove special characters except spaces and hyphens
        normalized = re.sub(r'[^a-z\s\-]', '', normalized)
        return normalized
    
    def _create_name_hash(self, name: str) -> str:
        """Create a hash of the normalized name for caching."""
        normalized = self._normalize_name(name)
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def _get_cached_result(self, name: str) -> Optional[WatchlistResult]:
        """Get cached validation result if still valid."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                name_hash = self._create_name_hash(name)
                
                cursor.execute("""
                    SELECT full_name, is_blocked, sources, confidence, reasons, raw_data, created_at
                    FROM watchlist_cache 
                    WHERE name_hash = ? AND expires_at > datetime('now')
                """, (name_hash,))
                
                row = cursor.fetchone()
                if row:
                    return WatchlistResult(
                        name=row[0],
                        is_blocked=bool(row[1]),
                        sources=json.loads(row[2]),
                        confidence=row[3],
                        reasons=json.loads(row[4]),
                        last_updated=datetime.fromisoformat(row[5]),
                        raw_data=json.loads(row[6])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
            return None
    
    def _cache_result(self, result: WatchlistResult):
        """Cache validation result."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                name_hash = self._create_name_hash(result.name)
                expires_at = datetime.now().replace(
                    hour=datetime.now().hour + self.cache_duration_hours
                ).isoformat()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO watchlist_cache 
                    (name_hash, full_name, is_blocked, sources, confidence, reasons, raw_data, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name_hash,
                    result.name,
                    result.is_blocked,
                    json.dumps(result.sources),
                    result.confidence,
                    json.dumps(result.reasons),
                    json.dumps(result.raw_data),
                    expires_at
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Cache storage failed: {e}")
    
    async def validate_name(self, name: str, category: str = "person") -> WatchlistResult:
        """Validate a name against all available watchlists."""
        logger.info(f"Validating name: {name} (category: {category})")
        
        # Check cache first
        cached_result = self._get_cached_result(name)
        if cached_result:
            logger.info(f"Using cached result for {name}")
            return cached_result
        
        # Initialize result
        result = WatchlistResult(
            name=name,
            is_blocked=False,
            sources=[],
            confidence=0.0,
            reasons=[],
            last_updated=datetime.now(),
            raw_data={}
        )
        
        # Validate against each source
        validation_tasks = []
        for source_name, source in self.sources.items():
            if source.enabled:
                task = self._validate_against_source(name, source_name, source, category)
                validation_tasks.append(task)
        
        # Execute all validations concurrently
        if validation_tasks:
            source_results = await asyncio.gather(*validation_tasks, return_exceptions=True)
            
            # Process results
            for source_name, source_result in zip(self.sources.keys(), source_results):
                if isinstance(source_result, Exception):
                    logger.error(f"Validation failed for {source_name}: {source_result}")
                    continue
                
                if source_result and source_result.get('is_blocked', False):
                    result.is_blocked = True
                    result.sources.append(source_name)
                    result.reasons.extend(source_result.get('reasons', []))
                    result.confidence = max(result.confidence, source_result.get('confidence', 0.0))
                
                result.raw_data[source_name] = source_result
        
        # Cache the result
        self._cache_result(result)
        
        logger.info(f"Validation completed for {name}: blocked={result.is_blocked}, confidence={result.confidence}")
        return result
    
    async def _validate_against_source(self, name: str, source_name: str, source: ValidationSource, category: str) -> Optional[Dict]:
        """Validate name against a specific source."""
        try:
            if source_name == "ofac_sdn":
                return await self._check_ofac_sdn(name, source)
            elif source_name == "fbi_wanted":
                return await self._check_fbi_wanted(name, source)
            elif source_name == "interpol_red":
                return await self._check_interpol_red(name, source)
            elif source_name == "un_sanctions":
                return await self._check_un_sanctions(name, source)
            elif source_name == "no_fly_list":
                return await self._check_no_fly_list(name, source)
            elif source_name == "national_sex_offender":
                return await self._check_sex_offender(name, source)
            elif source_name == "dru_sjodin_nsopw":
                return await self._check_dru_sjodin_nsopw(name, source)
            elif source_name == "murder_accountability_project":
                return await self._check_murder_accountability_project(name, source)
            elif source_name == "radford_serial_killer_db":
                return await self._check_radford_serial_killer_db(name, source)
            elif source_name == "european_sanctions":
                return await self._check_eu_sanctions(name, source)
            elif source_name == "uk_sanctions":
                return await self._check_uk_sanctions(name, source)
            elif source_name == "canada_sanctions":
                return await self._check_canada_sanctions(name, source)
            else:
                # Generic API call for other sources
                return await self._generic_api_check(name, source_name, source, category)
                
        except Exception as e:
            logger.error(f"Validation against {source_name} failed: {e}")
            return None
    
    async def _check_ofac_sdn(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against OFAC Specially Designated Nationals list."""
        if not source.api_key:
            logger.warning("OFAC API key not configured")
            return None
        
        try:
            params = {
                'api_key': source.api_key,
                'q': name,
                'type': 'Individual'
            }
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    for result in results:
                        if self._name_matches(name, result.get('name', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.9,
                                'reasons': [f"OFAC SDN: {result.get('programs', [])}"],
                                'source_data': result
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"OFAC API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"OFAC check failed: {e}")
            return None
    
    async def _check_fbi_wanted(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against FBI Most Wanted list."""
        try:
            params = {'title': name}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get('items', [])
                    
                    for item in items:
                        if self._name_matches(name, item.get('title', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.95,
                                'reasons': [f"FBI Most Wanted: {item.get('description', '')}"],
                                'source_data': item
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"FBI API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"FBI check failed: {e}")
            return None
    
    async def _check_interpol_red(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against Interpol Red Notices."""
        try:
            params = {'forename': name.split()[0], 'name': ' '.join(name.split()[1:])}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    notices = data.get('_embedded', {}).get('notices', [])
                    
                    for notice in notices:
                        if self._name_matches(name, notice.get('name', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.9,
                                'reasons': [f"Interpol Red Notice: {notice.get('arrest_warrants', [])}"],
                                'source_data': notice
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"Interpol API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Interpol check failed: {e}")
            return None
    
    async def _check_un_sanctions(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against UN Sanctions list."""
        try:
            async with self.session.get(source.url) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    # Parse XML and check for name matches
                    # This is a simplified implementation
                    if name.lower() in xml_content.lower():
                        return {
                            'is_blocked': True,
                            'confidence': 0.85,
                            'reasons': ["UN Sanctions List match"],
                            'source_data': {'xml_content': xml_content[:1000]}
                        }
                    
                    return {'is_blocked': False, 'confidence': 0.7}
                else:
                    logger.warning(f"UN Sanctions API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"UN Sanctions check failed: {e}")
            return None
    
    async def _check_no_fly_list(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against TSA No Fly List (public data)."""
        # Note: The actual No Fly List is not publicly accessible
        # This is a placeholder for demonstration purposes
        try:
            # Simulate checking against public TSA data
            # In reality, this would require special access
            return {
                'is_blocked': False,
                'confidence': 0.5,
                'reasons': ["No Fly List not publicly accessible"],
                'source_data': {'note': 'Requires special access'}
            }
        except Exception as e:
            logger.error(f"No Fly List check failed: {e}")
            return None
    
    async def _check_sex_offender(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against National Sex Offender Registry."""
        try:
            params = {'name': name}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    for result in results:
                        if self._name_matches(name, result.get('name', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.9,
                                'reasons': ["Sex Offender Registry match"],
                                'source_data': result
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"Sex Offender API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Sex Offender check failed: {e}")
            return None
    
    async def _check_dru_sjodin_nsopw(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against Dru Sjodin National Sex Offender Public Website (NSOPW)."""
        try:
            params = {'name': name}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    for result in results:
                        if self._name_matches(name, result.get('name', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.9,
                                'reasons': ["Dru Sjodin NSOPW Registry match"],
                                'source_data': result
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"Dru Sjodin NSOPW API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Dru Sjodin NSOPW check failed: {e}")
            return None
    
    async def _check_murder_accountability_project(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against Murder Accountability Project (MAP) database."""
        try:
            params = {'name': name}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    for result in results:
                        if self._name_matches(name, result.get('name', '')):
                            return {
                                'is_blocked': True,
                                'confidence': 0.95,
                                'reasons': [f"MAP Database: {result.get('description', 'Murder case match')}"],
                                'source_data': result
                            }
                    
                    return {'is_blocked': False, 'confidence': 0.8}
                else:
                    logger.warning(f"MAP API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"MAP check failed: {e}")
            return None
    
    async def _check_radford_serial_killer_db(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against Radford/FGCU Serial Killer Database."""
        try:
            # Radford database is typically accessed via web scraping or direct database access
            # This is a simplified implementation
            params = {'name': name}
            
            async with self.session.get(source.url, params=params) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Check if name appears in the database content
                    if name.lower() in content.lower():
                        return {
                            'is_blocked': True,
                            'confidence': 0.9,
                            'reasons': ["Radford Serial Killer Database match"],
                            'source_data': {'content': content[:1000]}
                        }
                    
                    return {'is_blocked': False, 'confidence': 0.7}
                else:
                    logger.warning(f"Radford Database returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Radford Serial Killer Database check failed: {e}")
            return None
    
    async def _check_eu_sanctions(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against EU Sanctions list."""
        try:
            async with self.session.get(source.url) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    if name.lower() in xml_content.lower():
                        return {
                            'is_blocked': True,
                            'confidence': 0.85,
                            'reasons': ["EU Sanctions List match"],
                            'source_data': {'xml_content': xml_content[:1000]}
                        }
                    
                    return {'is_blocked': False, 'confidence': 0.7}
                else:
                    logger.warning(f"EU Sanctions API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"EU Sanctions check failed: {e}")
            return None
    
    async def _check_uk_sanctions(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against UK Sanctions list."""
        try:
            # UK sanctions are typically in PDF format, would need special handling
            return {
                'is_blocked': False,
                'confidence': 0.5,
                'reasons': ["UK Sanctions List requires PDF parsing"],
                'source_data': {'note': 'Requires PDF processing'}
            }
        except Exception as e:
            logger.error(f"UK Sanctions check failed: {e}")
            return None
    
    async def _check_canada_sanctions(self, name: str, source: ValidationSource) -> Optional[Dict]:
        """Check against Canada Sanctions list."""
        try:
            async with self.session.get(source.url) as response:
                if response.status == 200:
                    content = await response.text()
                    if name.lower() in content.lower():
                        return {
                            'is_blocked': True,
                            'confidence': 0.85,
                            'reasons': ["Canada Sanctions List match"],
                            'source_data': {'content': content[:1000]}
                        }
                    
                    return {'is_blocked': False, 'confidence': 0.7}
                else:
                    logger.warning(f"Canada Sanctions API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Canada Sanctions check failed: {e}")
            return None
    
    async def _generic_api_check(self, name: str, source_name: str, source: ValidationSource, category: str) -> Optional[Dict]:
        """Generic API check for other sources."""
        try:
            headers = {}
            if source.api_key:
                headers['Authorization'] = f'Bearer {source.api_key}'
            
            params = {'name': name, 'category': category}
            
            async with self.session.get(source.url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Generic response parsing
                    if data.get('is_blocked', False):
                        return {
                            'is_blocked': True,
                            'confidence': data.get('confidence', 0.8),
                            'reasons': data.get('reasons', [f"{source_name} match"]),
                            'source_data': data
                        }
                    else:
                        return {
                            'is_blocked': False,
                            'confidence': data.get('confidence', 0.7),
                            'source_data': data
                        }
                else:
                    logger.warning(f"{source_name} API returned status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"{source_name} check failed: {e}")
            return None
    
    def _name_matches(self, input_name: str, watchlist_name: str) -> bool:
        """Check if input name matches watchlist name using fuzzy matching."""
        input_normalized = self._normalize_name(input_name)
        watchlist_normalized = self._normalize_name(watchlist_name)
        
        # Exact match
        if input_normalized == watchlist_normalized:
            return True
        
        # Split into parts for partial matching
        input_parts = set(input_normalized.split())
        watchlist_parts = set(watchlist_normalized.split())
        
        # Check for significant overlap (at least 2 parts match)
        overlap = input_parts.intersection(watchlist_parts)
        if len(overlap) >= 2:
            return True
        
        # Check for substring matches
        if input_normalized in watchlist_normalized or watchlist_normalized in input_normalized:
            return True
        
        return False
    
    def configure_api_key(self, source_name: str, api_key: str):
        """Configure API key for a specific source."""
        if source_name in self.sources:
            self.sources[source_name].api_key = api_key
            logger.info(f"API key configured for {source_name}")
        else:
            logger.warning(f"Unknown source: {source_name}")
    
    def enable_source(self, source_name: str, enabled: bool = True):
        """Enable or disable a validation source."""
        if source_name in self.sources:
            self.sources[source_name].enabled = enabled
            logger.info(f"Source {source_name} {'enabled' if enabled else 'disabled'}")
        else:
            logger.warning(f"Unknown source: {source_name}")
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get cache statistics
                cursor.execute("SELECT COUNT(*) FROM watchlist_cache")
                total_cached = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM watchlist_cache WHERE is_blocked = 1")
                total_blocked = cursor.fetchone()[0]
                
                # Get recent validation logs
                cursor.execute("""
                    SELECT COUNT(*) FROM validation_logs 
                    WHERE timestamp > datetime('now', '-24 hours')
                """)
                recent_validations = cursor.fetchone()[0]
                
                return {
                    'total_cached_results': total_cached,
                    'total_blocked_names': total_blocked,
                    'recent_validations_24h': recent_validations,
                    'enabled_sources': [name for name, source in self.sources.items() if source.enabled],
                    'cache_duration_hours': self.cache_duration_hours
                }
                
        except Exception as e:
            logger.error(f"Failed to get validation stats: {e}")
            return {}
    
    async def validate_batch(self, names: List[str], category: str = "person") -> List[WatchlistResult]:
        """Validate multiple names concurrently."""
        tasks = [self.validate_name(name, category) for name in names]
        return await asyncio.gather(*tasks)
    
    def clear_cache(self):
        """Clear all cached validation results."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM watchlist_cache")
                conn.commit()
                logger.info("Validation cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")


# Convenience function for standalone validation
async def validate_name_standalone(name: str, category: str = "person") -> WatchlistResult:
    """Standalone function to validate a name."""
    async with WatchlistValidator() as validator:
        return await validator.validate_name(name, category)


if __name__ == "__main__":
    # Example usage
    async def main():
        async with WatchlistValidator() as validator:
            # Configure API keys (if available)
            # validator.configure_api_key("ofac_sdn", "your_api_key_here")
            
            # Validate a name
            result = await validator.validate_name("John Smith", "person")
            print(f"Validation result: {result}")
            
            # Get statistics
            stats = validator.get_validation_stats()
            print(f"Validation stats: {stats}")
    
    asyncio.run(main())
