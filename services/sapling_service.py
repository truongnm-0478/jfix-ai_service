import requests
from config import Config

class SaplingService:
    """Service for integrating with Sapling API for grammar checking"""
    
    @staticmethod
    def check_japanese_grammar(text):
        """
        Check Japanese text for grammar issues using Sapling API
        
        Args:
            text (str): Japanese text to check
            
        Returns:
            dict: Result containing corrections and status
        """
        try:
            payload = {
                "key": Config.SAPLING_API_KEY,
                "session_id": "japanese_learning_app",
                "text": text,
                "lang": "ja"
            }
            
            response = requests.post(Config.SAPLING_API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "original_text": text,
                    "corrections": data.get("edits", []),
                    "corrected_text": apply_corrections(text, data.get("edits", []))
                }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}


def apply_corrections(text, edits):
    """
    Apply corrections to the original text
    
    Args:
        text (str): Original text
        edits (list): List of edits from Sapling API
        
    Returns:
        str: Corrected text
    """
    # Sort edits by position in reverse order to avoid offset issues
    edits = sorted(edits, key=lambda x: x.get("start", 0), reverse=True)
    
    # Apply each edit
    for edit in edits:
        start = edit.get("start", 0)
        end = edit.get("end", 0)
        replacement = edit.get("replacement", "")
        
        text = text[:start] + replacement + text[end:]
    
    return text