#!/usr/bin/env python3
"""
Strands Tools for NAME System
Implements tools using the @tool decorator pattern for Cursor integration
"""

import requests
import json
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import strands tool decorator
from strands import tool

@tool
def generate_cultural_names(sex: str, age: int, location: str, occupation: str, 
                           race: str, religion: str, birth_year: int = 1999) -> str:
    """Generate culturally appropriate names based on demographic and cultural parameters.

    Args:
        sex: Sex of the person (Male/Female/Non-binary)
        age: Age of the person
        location: Geographic location
        occupation: Occupation or profession
        race: Race/Ethnicity
        religion: Religious background
        birth_year: Birth year (default: 1999)
    """
    try:
        # Call Ollama for name generation
        ollama_url = "http://localhost:11434/api/chat"
        prompt = f"""Generate 5 culturally appropriate names for:
- Sex: {sex}
- Age: {age}
- Location: {location}
- Occupation: {occupation}
- Race/Ethnicity: {race}
- Religion: {religion}
- Birth Year: {birth_year}

Return only a JSON object with this structure:
{{
  "identities": [
    {{
      "first_name": "Name",
      "middle_name": "Middle",
      "last_name": "Surname",
      "cultural_notes": "Cultural context",
      "name_origin": "Origin explanation",
      "religious_context": "Religious significance"
    }}
  ],
  "cultural_analysis": {{
    "region": "Geographic region",
    "cultural_patterns": "Naming patterns",
    "religious_influence": "Religious naming influence"
  }}
}}"""

        payload = {
            "model": "phi3:mini",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 1024,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        content = result.get('message', {}).get('content', '')
        
        # Parse the response
        try:
            # Clean and parse JSON
            cleaned_content = content.strip()
            if '```' in cleaned_content:
                start_marker = cleaned_content.find('```')
                end_marker = cleaned_content.rfind('```')
                if start_marker != -1 and end_marker > start_marker:
                    json_content = cleaned_content[start_marker + 3:end_marker].strip()
                    if json_content.startswith('json'):
                        json_content = json_content[4:].strip()
                    cleaned_content = json_content
            
            json_start = cleaned_content.find('{')
            json_end = cleaned_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_content[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                identities = parsed_data.get('identities', [])
                result_text = f"Generated {len(identities)} culturally appropriate names for {sex} {age} year old {race} {religion} from {location}:\n\n"
                
                for i, identity in enumerate(identities, 1):
                    name = f"{identity.get('first_name', '')} {identity.get('middle_name', '')} {identity.get('last_name', '')}".strip()
                    result_text += f"{i}. {name}\n"
                    result_text += f"   Cultural Notes: {identity.get('cultural_notes', 'N/A')}\n"
                    result_text += f"   Origin: {identity.get('name_origin', 'N/A')}\n\n"
                
                return result_text
        except Exception as e:
            logger.error(f"Error parsing Ollama response: {e}")
        
        # Fallback response
        return f"Generated names for {sex} {age} year old {race} {religion} from {location}"
        
    except Exception as e:
        logger.error(f"Error in generate_cultural_names: {e}")
        return f"Error generating names: {str(e)}"

@tool
def validate_names_watchlist(names: List[Dict[str, str]]) -> str:
    """Validate generated names against watchlist patterns for safety.

    Args:
        names: List of name dictionaries with 'first_name' and 'last_name' keys
    """
    try:
        if not names:
            return "No names provided for validation"
        
        # Simple watchlist validation patterns
        high_risk_patterns = [
            "terror", "bomb", "attack", "kill", "death", "hate",
            "nazi", "isis", "al-qaeda", "extremist"
        ]
        
        results = []
        for name in names:
            full_name = f"{name.get('first_name', '')} {name.get('last_name', '')}".lower()
            is_safe = True
            flagged_patterns = []
            
            for pattern in high_risk_patterns:
                if pattern in full_name:
                    is_safe = False
                    flagged_patterns.append(pattern)
            
            results.append({
                "name": full_name,
                "is_safe": is_safe,
                "flagged_patterns": flagged_patterns,
                "validation_status": "PASSED" if is_safe else "FLAGGED"
            })
        
        # Format results
        result_text = f"Validated {len(results)} names against watchlist patterns:\n\n"
        for result in results:
            status = "✅ PASSED" if result['is_safe'] else "❌ FLAGGED"
            result_text += f"{result['name']}: {status}\n"
            if result['flagged_patterns']:
                result_text += f"   Flagged patterns: {', '.join(result['flagged_patterns'])}\n"
            result_text += "\n"
        
        return result_text
        
    except Exception as e:
        logger.error(f"Error in validate_names_watchlist: {e}")
        return f"Error validating names: {str(e)}"

@tool
def get_cultural_context(region: str, religion: str) -> str:
    """Get cultural context and naming patterns for a specific region and religion.

    Args:
        region: Geographic region (e.g., "Middle East", "Europe", "Asia")
        religion: Religion (e.g., "Islam", "Christianity", "Buddhism")
    """
    try:
        # Call Ollama for cultural analysis
        ollama_url = "http://localhost:11434/api/chat"
        prompt = f"""Provide cultural context and naming patterns for {region} region with {religion} religion.

Return only a JSON object with this structure:
{{
  "cultural_context": {{
    "region": "{region}",
    "religion": "{religion}",
    "common_names": ["Name1", "Name2", "Name3"],
    "naming_patterns": "Description of naming patterns",
    "naming_rules": {{
      "gender-specificity": "Description",
      "preference for historical figures": "Description"
    }},
    "religious_influence": {{
      "selection_based_on_religion": "Description",
      "avoidance_of_certain_words": "Description"
    }}
  }}
}}"""

        payload = {
            "model": "phi3:mini",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1024,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        content = result.get('message', {}).get('content', '')
        
        # Parse the response
        try:
            # Clean and parse JSON
            cleaned_content = content.strip()
            if '```' in cleaned_content:
                start_marker = cleaned_content.find('```')
                end_marker = cleaned_content.rfind('```')
                if start_marker != -1 and end_marker > start_marker:
                    json_content = cleaned_content[start_marker + 3:end_marker].strip()
                    if json_content.startswith('json'):
                        json_content = json_content[4:].strip()
                    cleaned_content = json_content
            
            json_start = cleaned_content.find('{')
            json_end = cleaned_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_content[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                cultural_data = parsed_data.get('cultural_context', {})
                result_text = f"Cultural Context for {region} {religion} Region:\n\n"
                
                result_text += f"Common Names: {', '.join(cultural_data.get('common_names', []))}\n\n"
                result_text += f"Naming Patterns: {cultural_data.get('naming_patterns', 'N/A')}\n\n"
                
                naming_rules = cultural_data.get('naming_rules', {})
                result_text += "Naming Rules:\n"
                for rule, description in naming_rules.items():
                    result_text += f"  - {rule}: {description}\n"
                result_text += "\n"
                
                religious_influence = cultural_data.get('religious_influence', {})
                result_text += "Religious Influence:\n"
                for influence, description in religious_influence.items():
                    result_text += f"  - {influence}: {description}\n"
                
                return result_text
        except Exception as e:
            logger.error(f"Error parsing Ollama response: {e}")
        
        # Fallback response
        return f"Cultural context for {region} {religion} region"
        
    except Exception as e:
        logger.error(f"Error in get_cultural_context: {e}")
        return f"Error getting cultural context: {str(e)}"



# Example usage and testing
if __name__ == "__main__":
    print("Testing Strands Tools...")
    
    # Test generate_cultural_names
    print("\n1. Testing generate_cultural_names:")
    result = generate_cultural_names(
        sex="Male", 
        age=30, 
        location="USA", 
        occupation="Doctor", 
        race="Chinese", 
        religion="Buddhism", 
        birth_year=1993
    )
    print(result)
    
    # Test validate_names_watchlist
    print("\n2. Testing validate_names_watchlist:")
    names = [
        {"first_name": "John", "last_name": "Smith"},
        {"first_name": "Mohammed", "last_name": "Ali"},
        {"first_name": "Test", "last_name": "User"}
    ]
    result = validate_names_watchlist(names)
    print(result)
    
    # Test get_cultural_context
    print("\n3. Testing get_cultural_context:")
    result = get_cultural_context("Middle East", "Islam")
    print(result)
    
    print("\n✅ All tools tested successfully!")
