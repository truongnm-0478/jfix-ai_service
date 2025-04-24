import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the application"""
    SAPLING_API_KEY = os.getenv('SAPLING_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    SAPLING_API_URL = "https://api.sapling.ai/api/v1/edits"
    
    # Default prompts for Gemini
    DEFAULT_JAPANESE_CONVERSATION_PROMPT = """
    あなたは日本語会話の先生です。以下のテーマについて、初級レベルの学習者と会話してください。
    簡単な質問をして、学習者が答えやすいように導いてください。
    文法的な間違いがあれば、優しく訂正してください。
    テーマ: {theme}
    """