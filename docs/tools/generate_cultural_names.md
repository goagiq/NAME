Tool Card: generate_cultural_names

General Info

    Name: generate_cultural_names
    Title: Cultural Name Generator
    Version: 1.0.0
    Author: NAME System Team
    Description: Generates culturally appropriate names based on user-specified cultural parameters using Ollama LLM.

Required Libraries

    requests>=2.25.0
    json
    logging
    typing (Dict, List, Any, Optional)
    sys
    os

Imports and Decorators

    import json
    import logging
    from typing import Dict, List, Any, Optional
    import sys
    import os

    # Add src to path for imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    from services.ollama_cultural_service import OllamaCulturalService

    logger = logging.getLogger(__name__)

    # Initialize the Ollama service
    ollama_service = OllamaCulturalService()

    # MCP Tool Decorator (if applicable)
    # @tool("generate_cultural_names")

Intended Use

    For conversational agents and applications needing culturally authentic name generation.
    Supports multiple cultural contexts including race, religion, location, and demographic factors.
    Generates complete identities with first, middle, and last names.

Out-of-Scope / Limitations

    Requires Ollama LLM service to be running on localhost:11434.
    Limited to supported cultural combinations in the training data.
    Generation quality depends on the underlying LLM model.
    No guarantee of name uniqueness across calls.

Input Schema

{
  "type": "object",
  "properties": {
    "race": {
      "type": "string",
      "description": "Ethnicity/race of the person (e.g., 'asian', 'african', 'caucasian')"
    },
    "religion": {
      "type": "string", 
      "description": "Religious background (e.g., 'christian', 'muslim', 'hindu')"
    },
    "location": {
      "type": "string",
      "description": "Geographic location or region"
    },
    "birth_country": {
      "type": "string",
      "description": "Country of birth"
    },
    "sex": {
      "type": "string",
      "enum": ["person", "male", "female"],
      "description": "Gender of the person"
    },
    "age": {
      "type": "string",
      "description": "Age of the person"
    },
    "birth_year": {
      "type": "string", 
      "description": "Year of birth"
    }
  },
  "required": ["race", "religion", "location"]
}

Output Schema

{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "first_name": {
        "type": "string",
        "description": "Generated first name"
      },
      "middle_name": {
        "type": "string", 
        "description": "Generated middle name"
      },
      "last_name": {
        "type": "string",
        "description": "Generated last name"
      },
      "cultural_context": {
        "type": "string",
        "description": "Cultural background explanation"
      },
      "confidence_score": {
        "type": "number",
        "description": "Confidence in cultural appropriateness (0-1)"
      }
    },
    "required": ["first_name", "last_name", "cultural_context"]
  }
}

Example

    Input:
    {
      "race": "asian",
      "religion": "buddhist", 
      "location": "thailand",
      "sex": "male",
      "age": "25",
      "birth_year": "1998"
    }
    
    Output:
    [
      {
        "first_name": "Somchai",
        "middle_name": "Prasert",
        "last_name": "Srisuwan",
        "cultural_context": "Traditional Thai Buddhist naming with respect for cultural heritage",
        "confidence_score": 0.92
      },
      {
        "first_name": "Ananda",
        "middle_name": "Chai",
        "last_name": "Rattanakul",
        "cultural_context": "Thai Buddhist name meaning 'bliss' with traditional surname",
        "confidence_score": 0.89
      }
    ]

Safety & Reliability

    Validates all input parameters against schema requirements.
    Returns error JSON if Ollama service is unavailable.
    Includes fallback name generation if LLM fails.
    No PII storage; all data processed in memory only.
    Logs errors for debugging but not user data.
