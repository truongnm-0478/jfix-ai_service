from flask import request
from flask_restful import Resource
from services.gemini_service import GeminiService

class ConversationResource(Resource):
    """API endpoint for generating Japanese conversations"""
    
    def post(self):
        """
        POST endpoint for generating conversation starters
        
        Expected JSON payload:
        {
            "user_id": "unique_user_identifier",
            "theme": "conversation theme",
            "level": "N5/N4/N3/N2/N1",
            "conversation_history": [],  # Optional previous messages
            "user_input": "Japanese input from user"
        }
        """
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return {"error": "Missing user_id"}, 400
            
        if 'theme' not in data or 'user_input' not in data:
            return {"error": "Missing required fields"}, 400
        
        gemini_service = GeminiService()
        
        # Get optional parameters with defaults
        level = data.get('level', 'N4')
        conversation_history = data.get('conversation_history', [])
        
        result = gemini_service.generate_japanese_conversation(
            user_id=data['user_id'],
            topic=data['theme'],
            user_level=level,
            conversation_history=conversation_history,
            user_input=data['user_input']
        )
        
        if result['status'] == 'success':
            return result, 200
        else:
            return result, 500
        
class ConversationHistoryResource(Resource):
    """API endpoint for retrieving conversation history"""
    
    def get(self):
        """
        GET endpoint for retrieving conversation history
        
        Expected query parameters:
        - user_id: Unique identifier for the user
        - limit: (Optional) Maximum number of conversation exchanges to return
        """
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', default=10, type=int)
        
        if not user_id:
            return {"error": "Missing user_id parameter"}, 400
        
        gemini_service = GeminiService()
        result = gemini_service.get_conversation_history(user_id, limit)
        
        if result['status'] == 'success':
            return result, 200
        else:
            return result, 500