from flask import request
from flask_restful import Resource
from services.sapling_service import SaplingService

class GrammarCheckResource(Resource):
    """API endpoint for checking Japanese grammar"""
    
    def post(self):
        """
        POST endpoint for grammar checking
        
        Expected JSON payload:
        {
            "text": "Japanese text to check"
        }
        """
        data = request.get_json()
        
        if not data or 'text' not in data:
            return {"error": "Missing text"}, 400
        
        result = SaplingService.check_japanese_grammar(data['text'])
        
        if result['status'] == 'success':
            return result, 200
        else:
            return result, 500