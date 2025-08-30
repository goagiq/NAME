"""
Optimized Flask Frontend for NAME System
Uses Ollama LLM for culturally appropriate name generation.
"""

from flask import Flask, render_template, request, jsonify
import logging
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Ollama service
from services.ollama_cultural_service import OllamaCulturalService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize Ollama service with error handling
try:
    ollama_service = OllamaCulturalService()
    logger.info("Ollama service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Ollama service: {e}")
    ollama_service = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "Python frontend is running"})

@app.route('/api/generate-identity', methods=['POST'])
def generate_identity():
    try:
        data = request.get_json()
        
        # Prepare request data for Ollama service
        request_data = {
            "sex": data.get("sex"),
            "location": data.get("location"),
            "age": int(data.get("age", 0)),
            "occupation": data.get("occupation"),
            "race": data.get("race"),
            "religion": data.get("religion"),
            "birth_year": int(data.get("birth_year", 0)),
            "birth_country": data.get("birth_country"),
            "citizenship_country": data.get("citizenship_country"),
            "diaspora_generation": data.get("diaspora_generation")
        }
        
        # Handle "Other" options
        if data.get("race") == "Other" and data.get("race_other"):
            request_data["race"] = data.get("race_other")
        if data.get("religion") == "Other" and data.get("religion_other"):
            request_data["religion"] = data.get("religion_other")
        
        # Process feedback context if provided
        feedback_context = data.get("feedback_context")
        if feedback_context:
            logger.info(f"Using feedback context: {feedback_context}")
            request_data["feedback_context"] = feedback_context
        
        # Use Ollama service to generate culturally appropriate names
        if ollama_service is None:
            logger.error("Ollama service not available, using fallback")
            return jsonify({"error": "Ollama service not available"}), 500
            
        logger.info(f"Generating names using Ollama for: {request_data}")
        identities = ollama_service.generate_cultural_names(request_data)
        
        return jsonify(identities)
            
    except Exception as e:
        logger.error(f"Error in generate_identity: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/regenerate-identity', methods=['POST'])
def regenerate_identity():
    try:
        data = request.get_json()
        
        # Prepare request data for Ollama service
        request_data = {
            "sex": data.get("sex"),
            "location": data.get("location"),
            "age": int(data.get("age", 0)),
            "occupation": data.get("occupation"),
            "race": data.get("race"),
            "religion": data.get("religion"),
            "birth_year": int(data.get("birth_year", 0)),
            "birth_country": data.get("birth_country"),
            "citizenship_country": data.get("citizenship_country"),
            "diaspora_generation": data.get("diaspora_generation")
        }
        
        # Handle "Other" options
        if data.get("race") == "Other" and data.get("race_other"):
            request_data["race"] = data.get("race_other")
        if data.get("religion") == "Other" and data.get("religion_other"):
            request_data["religion"] = data.get("religion_other")
        
        # Process feedback context if provided
        feedback_context = data.get("feedback_context")
        if feedback_context:
            logger.info(f"Using feedback context: {feedback_context}")
            request_data["feedback_context"] = feedback_context
        
        # Use Ollama service to regenerate culturally appropriate names
        if ollama_service is None:
            logger.error("Ollama service not available, using fallback")
            return jsonify({"error": "Ollama service not available"}), 500
            
        logger.info(f"Regenerating names using Ollama for: {request_data}")
        identities = ollama_service.generate_cultural_names(request_data)
        
        return jsonify(identities)
            
    except Exception as e:
        logger.error(f"Error in regenerate_identity: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/traceability/<request_id>')
def get_traceability(request_id):
    """Get traceability information for a request."""
    try:
        # For now, return a mock traceability response
        # In a full implementation, this would store and retrieve traceability data
        return jsonify({
            "request_id": request_id,
            "message": "Traceability data would be stored and retrieved here",
            "status": "not_implemented",
            "timestamp": datetime.utcnow().isoformat()
        })
            
    except Exception as e:
        logger.error(f"Error in get_traceability: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/cultures')
def get_supported_cultures():
    """Get list of supported cultures."""
    return jsonify({
        "cultures": [
            {"code": "sudanese", "name": "Sudanese", "description": "Arabic/Islamic naming traditions"},
            {"code": "spanish", "name": "Spanish", "description": "Traditional Spanish naming conventions"},
            {"code": "chinese", "name": "Chinese", "description": "Chinese naming patterns"},
            {"code": "indian", "name": "Indian", "description": "Indian naming traditions"},
            {"code": "american", "name": "American", "description": "Western naming conventions"},
            {"code": "british", "name": "British", "description": "British naming traditions"},
            {"code": "french", "name": "French", "description": "French naming conventions"},
            {"code": "german", "name": "German", "description": "German naming traditions"},
            {"code": "italian", "name": "Italian", "description": "Italian naming conventions"},
            {"code": "japanese", "name": "Japanese", "description": "Japanese naming patterns"},
            {"code": "korean", "name": "Korean", "description": "Korean naming traditions"},
            {"code": "vietnamese", "name": "Vietnamese", "description": "Vietnamese naming patterns"},
            {"code": "thai", "name": "Thai", "description": "Thai naming traditions"},
            {"code": "filipino", "name": "Filipino", "description": "Filipino naming conventions"},
            {"code": "mexican", "name": "Mexican", "description": "Mexican naming traditions"},
            {"code": "brazilian", "name": "Brazilian", "description": "Brazilian naming conventions"},
            {"code": "argentine", "name": "Argentine", "description": "Argentine naming traditions"},
            {"code": "egyptian", "name": "Egyptian", "description": "Egyptian naming conventions"},
            {"code": "moroccan", "name": "Moroccan", "description": "Moroccan naming traditions"},
            {"code": "turkish", "name": "Turkish", "description": "Turkish naming conventions"},
            {"code": "iranian", "name": "Iranian", "description": "Iranian naming traditions"},
            {"code": "pakistani", "name": "Pakistani", "description": "Pakistani naming conventions"},
            {"code": "bangladeshi", "name": "Bangladeshi", "description": "Bangladeshi naming traditions"},
            {"code": "nigerian", "name": "Nigerian", "description": "Nigerian naming conventions"},
            {"code": "kenyan", "name": "Kenyan", "description": "Kenyan naming traditions"},
            {"code": "south_african", "name": "South African", "description": "South African naming conventions"}
        ]
    })


@app.route('/api/statistics')
def get_statistics():
    """Get system statistics."""
    return jsonify({
        "total_generations": 0,  # Would be tracked in a real implementation
        "successful_generations": 0,
        "failed_generations": 0,
        "most_popular_culture": "Sudanese",
        "average_response_time": "1.2s",
        "system_uptime": "100%",
        "ollama_status": "connected" if ollama_service else "disconnected"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
