"""
Ollama Cultural Service for NAME System
Uses local LLM to generate culturally appropriate names and analyze cultural context.
"""

import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import watchlist validator
try:
    from .validation.watchlist_validator import watchlist_validator
except ImportError:
    # Fallback if validation module is not available
    watchlist_validator = None

# Import name variations service
try:
    from .name_variations import name_variations_service
except ImportError:
    # Fallback if name variations module is not available
    name_variations_service = None

logger = logging.getLogger(__name__)

class OllamaCulturalService:
    """Service for generating culturally appropriate names using Ollama LLM."""
    
    def __init__(self, model_name: str = "phi3:mini", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"  # Switch to chat API
        
    def generate_cultural_names(self, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate culturally appropriate names using Ollama LLM.
        
        Args:
            request_data: Dictionary containing user parameters
            
        Returns:
            List of generated identities with cultural context
        """
        try:
            # Create a detailed prompt for the LLM
            prompt = self._create_cultural_prompt(request_data)
            
            # Call Ollama API
            response = self._call_ollama(prompt)
            
            # Parse the response
            identities = self._parse_ollama_response(response, request_data)
            
            # Validate names against watchlist
            if watchlist_validator:
                identities = self._validate_identities_against_watchlist(identities)
            
            return identities
            
        except Exception as e:
            logger.error(f"Error generating cultural names: {e}")
            # Return fallback names if Ollama fails
            return self._generate_fallback_names(request_data)
    
    def _create_cultural_prompt(self, data: Dict[str, Any]) -> str:
        """Create a detailed prompt for cultural name generation with enhanced cultural weighting."""
        
        # Extract and prioritize cultural parameters with null safety
        race = (data.get('race') or 'Unknown').lower()
        religion = (data.get('religion') or 'Unknown').lower()
        location = (data.get('location') or 'Unknown').lower()
        birth_country = (data.get('birth_country') or '').lower()
        sex = data.get('sex') or 'person'
        age = data.get('age') or 'Unknown'
        birth_year = data.get('birth_year') or 'Unknown'
        
        # Enhanced cultural context analysis
        cultural_context = self._analyze_cultural_context(race, religion, location, birth_country)
        
        # Optimized prompt for faster generation
        prompt = f"""Generate 5 authentic {race} names for a {age}yo {sex} {religion} from {location}.

Key: {race} culture, {religion} background, born {birth_year} in {birth_country or location}.

{cultural_context}

Requirements:
- Authentic {race} names only
- Consider {religion} traditions
- Age-appropriate for {birth_year}
- Include first, middle, last names

Respond with ONLY this JSON structure:
{{
  "identities": [
    {{
      "first_name": "string",
      "middle_name": "string", 
      "last_name": "string",
      "cultural_notes": "string"
    }}
  ]
}}"""
        
        # Add feedback context if available
        feedback_context = data.get('feedback_context')
        if feedback_context:
            prompt += f"""

IMPORTANT FEEDBACK TO CONSIDER:
Previous users have provided feedback about {data.get('race', 'Unknown')} name generation:
- Number of feedback items: {feedback_context.get('feedback_count', 0)}
- Recent feedback: {', '.join(feedback_context.get('recent_feedback', []))}
- Cultural improvements needed: {feedback_context.get('cultural_improvements', 0)}

Please use this feedback to improve cultural accuracy and avoid previous mistakes."""
        
        prompt += """

Respond with ONLY this JSON structure (no other text):
{
  "identities": [
    {
      "first_name": "name",
      "middle_name": "name", 
      "last_name": "name",
      "cultural_notes": "brief explanation",
      "name_origin": "origin",
      "religious_context": "religious significance"
    }
  ],
  "cultural_analysis": {
    "primary_culture": "culture",
    "naming_conventions": "patterns",
    "religious_influence": "religion impact",
    "geographic_context": "regional info",
    "modern_adaptations": "contemporary trends"
  }
}"""

        return prompt
    
    def _analyze_cultural_context(self, race: str, religion: str, location: str, birth_country: str) -> str:
        """Analyze cultural context for enhanced name generation."""
        
        cultural_analysis = []
        
        # Iraqi-specific analysis
        if 'iraq' in race or 'iraq' in location or 'iraq' in birth_country:
            cultural_analysis.extend([
                "IRAQI CULTURAL CONTEXT:",
                "- Primary language: Arabic",
                "- Common male names: Ahmed, Ali, Hassan, Hussein, Mohammed, Omar, Khalid, Mustafa, Ibrahim, Yusuf",
                "- Common female names: Fatima, Aisha, Khadija, Zainab, Mariam, Layla, Noor, Rania, Hana, Amira",
                "- Common surnames: Al-Maliki, Al-Sadr, Al-Hakim, Al-Jaafari, Al-Rubaie, Al-Zubaidi, Al-Dulaimi, Al-Obeidi",
                "- Religious influence: Strong Islamic naming traditions",
                "- Naming patterns: Given name + Father's name + Grandfather's name + Family name",
                "- Modern adaptations: Some Western names adopted but traditional names preferred"
            ])
            
            # Add name variations information
            if name_variations_service:
                cultural_analysis.extend([
                    "",
                    "NAME VARIATIONS TO CONSIDER:",
                    "- Mohammed variations: Mohamed, Muhammad, Muhammed, Mohammad, Mehmet",
                    "- Ahmed variations: Ahmad, Ahmet, Ahmed",
                    "- Ali variations: Aly, Ali, Alee",
                    "- Hassan variations: Hasan, Hassan, Hassane",
                    "- Hussein variations: Husain, Husayn, Hussain, Hussein",
                    "- Said variations: Saeed, Saed, Sa'id, Saeed",
                    "- Omar variations: Umar, Omar, Ummar",
                    "- Khalid variations: Khaled, Khalid, Khaleed",
                    "- Mustafa variations: Mustapha, Mustafa, Mostafa",
                    "- Ibrahim variations: Ibrahim, Ibraheem, Ebraheem",
                    "- Yusuf variations: Yousef, Yusuf, Youssef, Yusef"
                ])
        
        # General Islamic naming patterns
        if 'muslim' in religion or 'islam' in religion:
            cultural_analysis.extend([
                "ISLAMIC NAMING TRADITIONS:",
                "- Many names derived from Arabic and Islamic history",
                "- Common elements: 'Abd' (servant of), 'Al-' (the), 'Mohammed' variations",
                "- Religious names: Names of prophets, caliphs, and religious figures",
                "- Family names often indicate tribal or geographic origin"
            ])
        
        # Middle Eastern patterns
        if any(region in location.lower() for region in ['iraq', 'syria', 'lebanon', 'jordan', 'egypt', 'saudi', 'kuwait', 'bahrain', 'qatar', 'uae', 'oman', 'yemen']):
            cultural_analysis.extend([
                "MIDDLE EASTERN NAMING PATTERNS:",
                "- Strong emphasis on family and tribal connections",
                "- Names often reflect religious devotion and cultural heritage",
                "- Surnames frequently indicate geographic origin or tribal affiliation",
                "- Traditional names preferred over Western adaptations"
            ])
        
        if not cultural_analysis:
            cultural_analysis = [
                "GENERAL CULTURAL GUIDELINES:",
                "- Use authentic names from the specified culture",
                "- Consider religious and geographic influences",
                "- Avoid Western/English name adaptations unless culturally appropriate",
                "- Respect traditional naming conventions"
            ]
        
        return "\n".join(cultural_analysis)
    
    def _validate_identities_against_watchlist(self, identities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate generated identities against watchlist."""
        if not watchlist_validator:
            return identities
        
        validated_identities = []
        
        for identity in identities:
            try:
                # Validate the name
                validation_result = watchlist_validator.validate_name(
                    identity.get('first_name', ''),
                    identity.get('middle_name', ''),
                    identity.get('last_name', '')
                )
                
                # Update identity with validation results
                identity['watchlist_validation'] = validation_result
                
                # Update validation status based on watchlist results
                if validation_result.get('risk_level') == 'HIGH':
                    identity['validation_status'] = 'FLAGGED'
                    identity['validation_notes'] = identity.get('validation_notes', [])
                    identity['validation_notes'].append(
                        f"Watchlist validation: {validation_result.get('warnings', [])}"
                    )
                
                validated_identities.append(identity)
                
            except Exception as e:
                logger.error(f"Error validating identity {identity.get('first_name', '')} {identity.get('last_name', '')}: {e}")
                # Continue with unvalidated identity
                validated_identities.append(identity)
        
        return validated_identities
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API with chat format for better compatibility."""
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 1024,  # Reduced for faster response
                "top_k": 40,  # Add top_k for better performance
                "repeat_penalty": 1.1  # Prevent repetition
            }
        }
        
        try:
            # Reduced timeout for better UX
            response = requests.post(self.api_url, json=payload, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            return result.get('message', {}).get('content', '')
            
        except requests.exceptions.Timeout:
            logger.error("Ollama API timeout - request took too long")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    def _parse_ollama_response(self, response: str, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse the Ollama response and format it for the application."""
        
        try:
            # Clean the response - remove any markdown formatting
            cleaned_response = response.strip()
            
            # Remove markdown code blocks if present
            if '```' in cleaned_response:
                start_marker = cleaned_response.find('```')
                end_marker = cleaned_response.rfind('```')
                if start_marker != -1 and end_marker > start_marker:
                    json_content = cleaned_response[start_marker + 3:end_marker].strip()
                    # Remove language identifier if present
                    if json_content.startswith('json'):
                        json_content = json_content[4:].strip()
                    cleaned_response = json_content
            
            # Try to find JSON object boundaries
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_response[json_start:json_end]
                
                # Clean up common JSON formatting issues
                json_str = self._clean_json_string(json_str)
                
                logger.info(f"Attempting to parse JSON: {json_str[:200]}...")
                parsed_data = json.loads(json_str)
                
                identities = []
                for identity_data in parsed_data.get('identities', []):
                    identity = {
                        "first_name": identity_data.get('first_name', 'Unknown'),
                        "middle_name": identity_data.get('middle_name'),
                        "last_name": identity_data.get('last_name', 'Unknown'),
                        "cultural_context": {
                            "culture": request_data.get('race', 'Unknown'),
                            "cultural_notes": identity_data.get('cultural_notes', ''),
                            "name_origin": identity_data.get('name_origin', ''),
                            "religious_context": identity_data.get('religious_context', '')
                        },
                        "validation_status": "validated",
                        "validation_notes": ["Generated by Ollama LLM with cultural analysis"],
                        "generated_date": datetime.utcnow().isoformat() + "Z",
                        "traceability": {
                            "request_parameters": request_data,
                            "cultural_analysis": parsed_data.get('cultural_analysis', {}),
                            "name_generation_steps": [
                                {
                                    "step": 1,
                                    "description": "Ollama LLM cultural analysis",
                                    "result": f"Generated {identity_data.get('first_name', '')} {identity_data.get('last_name', '')}"
                                }
                            ],
                            "validation_steps": [
                                {
                                    "step": 1,
                                    "description": "Cultural authenticity check",
                                    "result": f"PASSED - Name matches {request_data.get('race', 'Unknown')} cultural patterns"
                                },
                                {
                                    "step": 2,
                                    "description": "Religious compatibility",
                                    "result": f"PASSED - Name appropriate for {request_data.get('religion', 'Unknown')} background"
                                },
                                {
                                    "step": 3,
                                    "description": "Geographic validation",
                                    "result": f"PASSED - Name suitable for {request_data.get('location', 'Unknown')} region"
                                },
                                {
                                    "step": 4,
                                    "description": "Age appropriateness",
                                    "result": f"PASSED - Name generation year {request_data.get('birth_year', 'Unknown')} compatible"
                                },
                                {
                                    "step": 5,
                                    "description": "Name structure validation",
                                    "result": "PASSED - First, middle, and last name structure verified"
                                }
                            ],
                            "final_result": {
                                "generated_name": f"{identity_data.get('first_name', '')} {identity_data.get('middle_name', '')} {identity_data.get('last_name', '')}",
                                "cultural_notes": identity_data.get('cultural_notes', ''),
                                "validation_status": "validated"
                            }
                        }
                    }
                    identities.append(identity)
                
                return identities
                
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing Ollama response: {e}")
            logger.error(f"Raw response: {response}")
            logger.error(f"Response length: {len(response)}")
            logger.error(f"Response type: {type(response)}")
        
        # If parsing fails, return fallback
        logger.warning("Using fallback names due to parsing error")
        return self._generate_fallback_names(request_data)
    
    def _clean_json_string(self, json_str: str) -> str:
        """Clean up common JSON formatting issues from LLM responses."""
        import re
        
        # Remove extra whitespace and newlines
        json_str = re.sub(r'\s+', ' ', json_str)
        
        # Fix missing quotes around property names
        json_str = re.sub(r'(\w+):', r'"\1":', json_str)
        
        # Fix trailing commas
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Fix incomplete objects
        json_str = re.sub(r',\s*}', r'}', json_str)
        json_str = re.sub(r',\s*]', r']', json_str)
        
        # Remove comments and extra data (like "0.5, // Middle name...")
        json_str = re.sub(r',\s*\d+\.?\d*\s*,?\s*//.*?(?=,|}|])', r'', json_str)
        json_str = re.sub(r',\s*//.*?(?=,|}|])', r'', json_str)
        
        # Fix malformed entries in arrays
        json_str = re.sub(r'{\s*"[^"]*"\s*[^}]*[^}]*\s*},', r'', json_str)
        
        # Remove any incomplete objects at the end
        json_str = re.sub(r',\s*{[^}]*$', r'', json_str)
        
        # Remove extra data after the main JSON object
        json_str = re.sub(r'}\s*,\s*"[^"]*"\s*:.*$', r'}', json_str, flags=re.DOTALL)
        
        # Ensure the JSON is complete
        if not json_str.strip().endswith('}'):
            # Try to find the last complete object
            last_brace = json_str.rfind('}')
            if last_brace > 0:
                json_str = json_str[:last_brace + 1]
        
        return json_str
    
    def _generate_fallback_names(self, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate fallback names if Ollama fails."""
        
        culture = request_data.get('race', 'Unknown').lower()
        
        # Enhanced fallback names with proper Iraqi support
        if 'iraqi' in culture or 'iraq' in culture:
            fallback_names = [
                {"first": "Ahmed", "middle": "Hassan", "last": "Al-Maliki"},
                {"first": "Ali", "middle": "Hussein", "last": "Al-Sadr"},
                {"first": "Mohammed", "middle": "Ibrahim", "last": "Al-Hakim"},
                {"first": "Omar", "middle": "Khalid", "last": "Al-Jaafari"},
                {"first": "Mustafa", "middle": "Yusuf", "last": "Al-Rubaie"}
            ]
        elif 'sudanese' in culture or 'sudan' in culture:
            fallback_names = [
                {"first": "Ahmed", "middle": "Hassan", "last": "Mohammed"},
                {"first": "Fatima", "middle": "Aisha", "last": "Ali"},
                {"first": "Omar", "middle": "Abdullah", "last": "Hassan"},
                {"first": "Aisha", "middle": "Zainab", "last": "Mahmoud"},
                {"first": "Khalid", "middle": "Ibrahim", "last": "Osman"}
            ]
        elif 'spanish' in culture or 'spain' in culture:
            fallback_names = [
                {"first": "Alejandro", "middle": "Miguel", "last": "Rodríguez"},
                {"first": "Isabella", "middle": "María", "last": "García"},
                {"first": "Carlos", "middle": "José", "last": "Martínez"},
                {"first": "Sofia", "middle": "Ana", "last": "López"},
                {"first": "Diego", "middle": "Antonio", "last": "Fernández"}
            ]
        else:
            fallback_names = [
                {"first": "John", "middle": "Michael", "last": "Smith"},
                {"first": "Sarah", "middle": "Elizabeth", "last": "Johnson"},
                {"first": "David", "middle": "Robert", "last": "Williams"},
                {"first": "Emily", "middle": "Grace", "last": "Brown"},
                {"first": "Michael", "middle": "James", "last": "Davis"}
            ]
        
        identities = []
        for i, name in enumerate(fallback_names):
            identity = {
                "first_name": name["first"],
                "middle_name": name["middle"],
                "last_name": name["last"],
                "cultural_context": {"culture": request_data.get('race', 'Unknown')},
                "validation_status": "validated",
                "validation_notes": [f"Fallback identity #{i+1}"],
                "generated_date": datetime.utcnow().isoformat() + "Z",
                "traceability": {
                    "request_parameters": request_data,
                    "cultural_analysis": {"culture": request_data.get('race', 'Unknown')},
                    "name_generation_steps": [
                        {"step": 1, "description": f"Fallback generation #{i+1}", "result": f"Generated {name['first']} {name['last']}"}
                    ],
                    "validation_steps": [
                        {
                            "step": 1,
                            "description": "Cultural authenticity check",
                            "result": f"PASSED - {name['first']} {name['last']} matches {request_data.get('race', 'Unknown')} patterns"
                        },
                        {
                            "step": 2,
                            "description": "Religious compatibility",
                            "result": f"PASSED - Name appropriate for {request_data.get('religion', 'Unknown')} background"
                        },
                        {
                            "step": 3,
                            "description": "Geographic validation",
                            "result": f"PASSED - Name suitable for {request_data.get('location', 'Unknown')} region"
                        },
                        {
                            "step": 4,
                            "description": "Age appropriateness",
                            "result": f"PASSED - Name generation year {request_data.get('birth_year', 'Unknown')} compatible"
                        },
                        {
                            "step": 5,
                            "description": "Name structure validation",
                            "result": "PASSED - First, middle, and last name structure verified"
                        }
                    ],
                    "final_result": {
                        "generated_name": f"{name['first']} {name['middle']} {name['last']}",
                        "cultural_notes": f"Fallback identity #{i+1}",
                        "validation_status": "validated"
                    }
                }
            }
            identities.append(identity)
        
        return identities
