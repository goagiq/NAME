Tool Card: get_cultural_context

General Info

    Name: get_cultural_context
    Title: Cultural Context Provider
    Version: 1.0.0
    Author: NAME System Team
    Description: Provides detailed cultural context information for specific combinations of race, religion, and location.

Intended Use

    For applications needing cultural background information for name generation.
    Provides insights into naming conventions and cultural practices.
    Supports educational and research applications requiring cultural context.

Out-of-Scope / Limitations

    Limited to supported cultural combinations in the knowledge base.
    Context information is static and may not reflect current cultural changes.
    No real-time cultural trend analysis.
    Focuses on naming conventions rather than broader cultural practices.

Input Schema

{
  "type": "object",
  "properties": {
    "race": {
      "type": "string",
      "description": "Ethnicity/race (e.g., 'asian', 'african', 'caucasian')"
    },
    "religion": {
      "type": "string",
      "description": "Religious background (e.g., 'christian', 'muslim', 'hindu')"
    },
    "location": {
      "type": "string",
      "description": "Geographic location or region"
    }
  },
  "required": ["race", "religion", "location"]
}

Output Schema

{
  "type": "object",
  "properties": {
    "race": {
      "type": "string",
      "description": "The race/ethnicity provided"
    },
    "religion": {
      "type": "string",
      "description": "The religion provided"
    },
    "location": {
      "type": "string",
      "description": "The location provided"
    },
    "cultural_notes": {
      "type": "string",
      "description": "General cultural background information"
    },
    "naming_conventions": {
      "type": "string",
      "description": "Specific naming conventions and practices"
    },
    "common_names": {
      "type": "string",
      "description": "Examples of common names in this cultural context"
    },
    "cultural_significance": {
      "type": "string",
      "description": "Cultural significance of names in this context"
    }
  },
  "required": ["race", "religion", "location", "cultural_notes", "naming_conventions"]
}

Example

    Input:
    {
      "race": "japanese",
      "religion": "shinto",
      "location": "tokyo"
    }
    
    Output:
    {
      "race": "japanese",
      "religion": "shinto",
      "location": "tokyo",
      "cultural_notes": "Japanese Shinto culture emphasizes harmony with nature and ancestral respect",
      "naming_conventions": "Japanese names typically follow surname-first order. Given names often reflect virtues, nature, or family wishes",
      "common_names": "Common Japanese surnames include Sato, Suzuki, Takahashi. Given names often end in -ko (girls) or -o (boys)",
      "cultural_significance": "Names in Shinto tradition often reflect natural elements, virtues, or family lineage. The choice of name is considered spiritually significant"
    }

Safety & Reliability

    Validates all required input parameters.
    Returns structured cultural information in consistent format.
    Handles unknown cultural combinations gracefully.
    No sensitive cultural information stored or logged.
    Provides educational content without cultural appropriation.
