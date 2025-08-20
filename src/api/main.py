"""
FastAPI Backend for Name Generation System
Provides REST API endpoints for the web UI.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import IdentityGenerator, IdentityRequest, GeneratedIdentity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Name Generation System API",
    description="API for generating culturally appropriate identities",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the identity generator
identity_generator = IdentityGenerator()


class IdentityRequestModel(BaseModel):
    """Pydantic model for identity request."""
    sex: str
    location: str
    age: int
    occupation: str
    race: str
    religion: str
    birth_year: int
    birth_country: Optional[str] = None
    citizenship_country: Optional[str] = None
    diaspora_generation: Optional[int] = None


class IdentityResponseModel(BaseModel):
    """Pydantic model for identity response."""
    first_name: str
    middle_name: Optional[str]
    last_name: str
    cultural_context: Dict[str, Any]
    validation_status: str
    validation_notes: List[str]
    generated_date: str
    traceability: Dict[str, Any]


class TraceabilityModel(BaseModel):
    """Pydantic model for traceability information."""
    request_parameters: Dict[str, Any]
    cultural_analysis: Dict[str, Any]
    name_generation_steps: List[Dict[str, Any]]
    validation_steps: List[Dict[str, Any]]
    final_result: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Name Generation System API",
        "version": "1.0.0",
        "endpoints": {
            "generate_identity": "/api/generate-identity",
            "regenerate_identity": "/api/regenerate-identity",
            "get_traceability": "/api/traceability/{request_id}",
            "mcp": "/mcp"
        }
    }


# MCP endpoints to handle MCP requests
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Handle MCP requests to prevent 404 errors."""
    logger.info(f"MCP endpoint received request: {request.method} {request.url}")
    return {
        "message": "MCP endpoint - Name Generation System",
        "status": "available",
        "tools": ["name_validation", "cultural_analysis", "identity_generation"]
    }


@app.get("/mcp")
async def mcp_get_endpoint():
    """Handle GET requests to MCP endpoint."""
    logger.info("MCP GET endpoint accessed")
    return {
        "message": "MCP endpoint - Name Generation System",
        "status": "available",
        "tools": ["name_validation", "cultural_analysis", "identity_generation"]
    }


@app.post("/api/generate-identity", response_model=List[IdentityResponseModel])
async def generate_identity(request: IdentityRequestModel):
    """
    Generate new identities based on user parameters.
    
    Args:
        request: Identity request parameters
        
    Returns:
        List of generated identities with traceability information
    """
    try:
        logger.info(f"Received identity generation request: {request}")
        
        # Convert to internal model
        identity_request = IdentityRequest(
            sex=request.sex,
            location=request.location,
            age=request.age,
            occupation=request.occupation,
            race=request.race,
            religion=request.religion,
            birth_year=request.birth_year,
            birth_country=request.birth_country,
            citizenship_country=request.citizenship_country,
            diaspora_generation=request.diaspora_generation
        )
        
        # Generate identities
        identities = identity_generator.generate_identity(identity_request)
        
        # Convert to response models with traceability
        response_identities = []
        for identity in identities:
            traceability = _generate_traceability(identity_request, identity)
            
            response_identity = IdentityResponseModel(
                first_name=identity.first_name,
                middle_name=identity.middle_name,
                last_name=identity.last_name,
                cultural_context=identity.cultural_context,
                validation_status=identity.validation_status,
                validation_notes=identity.validation_notes,
                generated_date=identity.generated_date.isoformat(),
                traceability=traceability
            )
            response_identities.append(response_identity)
        
        logger.info(f"Generated {len(response_identities)} identities")
        return response_identities
        
    except Exception as e:
        logger.error(f"Error generating identity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/regenerate-identity", response_model=List[IdentityResponseModel])
async def regenerate_identity(request: IdentityRequestModel):
    """
    Regenerate identities (same as generate but for regeneration requests).
    
    Args:
        request: Identity request parameters
        
    Returns:
        List of newly generated identities
    """
    return await generate_identity(request)


@app.get("/api/traceability/{request_id}")
async def get_traceability(request_id: str):
    """
    Get detailed traceability information for a specific request.
    
    Args:
        request_id: Unique identifier for the request
        
    Returns:
        Detailed traceability information
    """
    # In a real implementation, this would retrieve from database
    # For now, return a sample traceability report
    return {
        "request_id": request_id,
        "timestamp": "2024-01-01T12:00:00Z",
        "traceability": {
            "request_parameters": {
                "sex": "Male",
                "location": "Spain, Madrid",
                "age": 35,
                "occupation": "Software Engineer",
                "race": "Spanish",
                "religion": "Catholic",
                "birth_year": 1988
            },
            "cultural_analysis": {
                "culture": "Spanish",
                "region": "Madrid",
                "language": "Spanish",
                "religion": "Catholic",
                "naming_conventions": {
                    "uses_multiple_middle_names": True,
                    "maternal_paternal_surnames": True,
                    "formal_naming": True
                },
                "special_requirements": [
                    "multiple_middle_names",
                    "maternal_paternal_surnames"
                ]
            },
            "name_generation_steps": [
                {
                    "step": 1,
                    "description": "Cultural context analysis",
                    "result": "Spanish naming conventions identified"
                },
                {
                    "step": 2,
                    "description": "First name selection",
                    "result": "Selected 'Carlos' from Spanish male names"
                },
                {
                    "step": 3,
                    "description": "Middle name selection",
                    "result": "Selected 'Jose' from Spanish middle names"
                },
                {
                    "step": 4,
                    "description": "Surname generation",
                    "result": "Combined paternal 'Garcia' and maternal 'Rodriguez'"
                }
            ],
            "validation_steps": [
                {
                    "step": 1,
                    "description": "Watchlist check",
                    "result": "PASSED - No matches found"
                },
                {
                    "step": 2,
                    "description": "Accepted names check",
                    "result": "PASSED - Name not previously used"
                },
                {
                    "step": 3,
                    "description": "Cultural acceptability",
                    "result": "PASSED - Follows Spanish naming conventions"
                },
                {
                    "step": 4,
                    "description": "Special requirements",
                    "result": "PASSED - Includes middle name and dual surnames"
                }
            ],
            "final_result": {
                "generated_name": "Carlos Jose Garcia Rodriguez",
                "cultural_notes": "Spanish naming convention with paternal and maternal surnames",
                "validation_status": "validated",
                "confidence_score": 0.95
            }
        }
    }


def _generate_traceability(request: IdentityRequest, identity: GeneratedIdentity) -> Dict[str, Any]:
    """Generate traceability information for an identity."""
    # Use detailed traceability if available, otherwise fall back to basic
    if identity.detailed_traceability:
        return identity.detailed_traceability
    else:
        # Fallback to basic traceability
        return {
            "request_parameters": {
                "sex": request.sex,
                "location": request.location,
                "age": request.age,
                "occupation": request.occupation,
                "race": request.race,
                "religion": request.religion,
                "birth_year": request.birth_year,
                "birth_country": request.birth_country,
                "citizenship_country": request.citizenship_country,
                "diaspora_generation": request.diaspora_generation
            },
            "cultural_analysis": identity.cultural_context,
            "name_generation_steps": [
                {
                    "step": 1,
                    "description": "Cultural context analysis",
                    "result": f"Identified {identity.cultural_context.get('culture', 'Unknown')} culture"
                },
                {
                    "step": 2,
                    "description": "Name component selection",
                    "result": f"Selected components: {identity.first_name}, {identity.middle_name or 'None'}, {identity.last_name}"
                }
            ],
            "validation_steps": [
                {
                    "step": 1,
                    "description": "Comprehensive validation",
                    "result": f"Status: {identity.validation_status}"
                }
            ],
            "final_result": {
                "generated_name": f"{identity.first_name} {identity.middle_name or ''} {identity.last_name}".strip(),
                "cultural_notes": "Generated based on cultural context",
                "validation_status": identity.validation_status,
                "validation_notes": identity.validation_notes
            }
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
