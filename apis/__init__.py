from flask_restful import Api

def init_api(app):
    """Initialize API routes"""
    api = Api(app)
    
    # Import API resources
    from apis.speech_api import SpeechToTextResource, TextToSpeechResource
    from apis.grammar_api import GrammarCheckResource
    
    # Register API endpoints
    api.add_resource(SpeechToTextResource, '/api/speech-to-text')
    api.add_resource(TextToSpeechResource, '/api/text-to-speech')
    api.add_resource(GrammarCheckResource, '/api/grammar-check')
    return api