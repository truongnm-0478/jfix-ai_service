from flask import request
from flask_restful import Resource
from services.speech_service import SpeechService

class SpeechToTextResource(Resource):
    """API endpoint for converting speech to text"""
    
    def post(self):
        """
        POST endpoint for speech-to-text conversion
        
        Expected JSON payload:
        {
            "audio_data": "base64_encoded_audio",
            "language": "ja-JP"  # Optional, defaults to Japanese
        }
        """
        data = request.get_json()
        
        if not data or 'audio_data' not in data:
            return {"error": "Missing audio data"}, 400
        
        language = data.get('language', 'ja-JP')
        result = SpeechService.speech_to_text(data['audio_data'], language)
        
        if result['status'] == 'success':
            return result, 200
        else:
            return result, 500


class TextToSpeechResource(Resource):
    """API endpoint for converting text to speech"""
    
    def post(self):
        """
        POST endpoint for text-to-speech conversion
        
        Expected JSON payload:
        {
            "text": "Text to convert to speech",
            "language": "ja"  # Optional, defaults to Japanese
        }
        """
        data = request.get_json()
        
        if not data or 'text' not in data:
            return {"error": "Missing text"}, 400
        
        language = data.get('language', 'ja')
        result = SpeechService.text_to_speech(data['text'], language)
        
        if result['status'] == 'success':
            return result, 200
        else:
            return result, 500