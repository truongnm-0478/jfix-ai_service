from flask_restful import Api

def init_api(app):
    """Initialize API routes"""
    api = Api(app)
    
    # Import API resources
    from apis.speech_api import SpeechToTextResource, TextToSpeechResource
    
    # Register API endpoints
    api.add_resource(SpeechToTextResource, '/api/speech-to-text')
    api.add_resource(TextToSpeechResource, '/api/text-to-speech')
    
    return api