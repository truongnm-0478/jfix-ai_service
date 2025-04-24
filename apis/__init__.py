from flask_restful import Api

def init_api(app):
    """Initialize API routes"""
    api = Api(app)
    
    # Import API resources
    from apis.speech_api import SpeechToTextResource, TextToSpeechResource
    from apis.grammar_api import GrammarCheckResource
    from apis.conversation_api import ConversationResource, ConversationHistoryResource

    # Register API endpoints
    api.add_resource(SpeechToTextResource, '/api/speech-to-text')
    api.add_resource(TextToSpeechResource, '/api/text-to-speech')
    api.add_resource(GrammarCheckResource, '/api/grammar-check')
    api.add_resource(ConversationResource, '/api/conversation')
    api.add_resource(ConversationHistoryResource, '/api/conversation-history')
    return api