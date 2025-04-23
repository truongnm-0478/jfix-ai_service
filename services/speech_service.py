import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import base64


class SpeechService:
    """Service for handling speech-to-text and text-to-speech operations"""

    @staticmethod
    def speech_to_text(audio_data, language='ja-JP'):
        """
        Convert speech to text
        
        Args:
            audio_data (bytes): Base64 encoded audio data (can be mp3 or wav)
            language (str): Language code (default: Japanese)
            
        Returns:
            dict: Result containing text and status
        """
        try:
            # Decode base64 audio data
            decoded_audio = base64.b64decode(audio_data)
            
            # Save raw audio to a temporary file (assume it's MP3 or unknown)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_input_audio:
                temp_input_audio.write(decoded_audio)
                temp_input_path = temp_input_audio.name

            # Convert to WAV (PCM) format using pydub
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                audio_segment = AudioSegment.from_file(temp_input_path)
                audio_segment.export(temp_wav.name, format="wav")
                temp_wav_path = temp_wav.name

            # Speech recognition using WAV
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language)

            # Clean up temp files
            os.unlink(temp_input_path)
            os.unlink(temp_wav_path)
            
            return {"status": "success", "text": text}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def text_to_speech(text, language='ja'):
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (default: Japanese)
            
        Returns:
            dict: Result containing audio data and status
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(temp_audio.name)
                temp_audio_path = temp_audio.name
            
            # Read the audio file and convert to base64
            with open(temp_audio_path, "rb") as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # Clean up
            os.unlink(temp_audio_path)
            
            return {"status": "success", "audio_data": audio_data}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}