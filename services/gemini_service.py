import google.generativeai as genai
from config import Config
import json
import os
from datetime import datetime
from services.speech_service import SpeechService

class GeminiService:
    """Service for interacting with Google's Gemini API"""
    
    def __init__(self):
        """Initialize the Gemini service with API key"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # Get the generative model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Ensure conversations directory exists
        os.makedirs("data/conversations", exist_ok=True)
    
    def _get_conversation_file_path(self, user_id):
        """Get the file path for a user's conversation history"""
        return f"data/conversations/{user_id}_conversation.json"
    
    def _load_conversation_history(self, user_id):
        """Load conversation history for a user"""
        file_path = self._get_conversation_file_path(user_id)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading conversation history: {e}")
                return []
        return []
    
    def _save_conversation_history(self, user_id, conversation):
        """Save conversation history for a user"""
        file_path = self._get_conversation_file_path(user_id)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(conversation, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving conversation history: {e}")
    
    def _format_conversation_history(self, history):
        """Format conversation history for prompt"""
        if not history:
            return "Chưa có hội thoại trước đó."
        
        formatted = []
        for entry in history[-5:]:  # Use only the last 5 exchanges to keep context manageable
            if 'user_input' in entry:
                formatted.append(f"Người học: 「{entry['user_input']}」")
            if 'reply' in entry:
                formatted.append(f"Giáo viên: 「{entry['reply']}」")
                
        return "\n".join(formatted)
    
    def generate_japanese_conversation(self, user_id, topic, user_level, conversation_history, user_input):
        """
        Generate a Japanese conversation response based on user input
        
        Args:
            user_id (str): Unique identifier for the user
            topic (str): Conversation theme
            user_level (str): Japanese proficiency level (N5-N1)
            conversation_history (list): Previous conversation exchanges
            user_input (str): User's input in Japanese
            
        Returns:
            dict: Result containing the AI response and audio for reply
        """
        try:
            # If no conversation history provided in the request, load from storage
            if not conversation_history:
                conversation_history = self._load_conversation_history(user_id)
            
            # Check if the topic has changed (compare with the latest topic in history)
            previous_topic = None
            if conversation_history:
                previous_topic = conversation_history[-1].get('topic')

            # Format conversation history, but limit to recent exchanges
            formatted_history = self._format_conversation_history(conversation_history)
            
            # Prepare the prompt for Gemini, emphasizing the new topic
            prompt = f"""
            Bạn là giáo viên tiếng Nhật bản ngữ với kinh nghiệm dạy học sinh quốc tế. Nhiệm vụ của bạn là hỗ trợ người học Việt Nam luyện nói tiếng Nhật qua hội thoại tự nhiên.

            ## Ngữ cảnh:
            - Chủ đề hiện tại: {topic}
            - Trình độ: {user_level} (N5/N4/N3/N2/N1)
            - Hội thoại trước đó: {formatted_history}
            {'- Lưu ý: Người dùng đã chuyển sang chủ đề mới. Hãy tập trung vào chủ đề hiện tại và giảm ảnh hưởng của các chủ đề trước đó.' if previous_topic and previous_topic != topic else ''}

            ## Phát biểu của người học:
            「{user_input}」

            ## Yêu cầu kỹ thuật:
            Phản hồi dưới dạng JSON có cấu trúc sau:
            {{
            "correction": {{
                "hasError": boolean,
                "original": "câu gốc của người học",
                "suggestion": "câu sửa đúng (chỉ điền nếu hasError=true)",
                "explanation": "giải thích lỗi bằng tiếng Việt, hoặc 'Câu đúng, rất tự nhiên!' nếu không có lỗi"
            }},
            "reply": "phản hồi tự nhiên bằng tiếng Nhật + câu hỏi để tiếp tục hội thoại",
            "vocabulary": [
                {{
                "word": "từ vựng đáng chú ý trong câu trả lời",
                "reading": "cách đọc",
                "meaning": "nghĩa tiếng Việt"
                }}
            ]
            }}

            ## Nguyên tắc:
            1. Sử dụng ĐÚNG JSON format, không thêm text ngoài JSON
            2. Viết tiếng Việt TRONG phần correction.explanation và vocabulary.meaning
            3. Viết tiếng Nhật TRONG phần reply
            4. Điều chỉnh độ khó của câu - Nếu không có lỗi, để suggestion là chuỗi rỗng
            5. Tập trung vào lỗi ngữ pháp quan trọng nhất, tránh sửa quá nhiều
            6. Phản hồi bằng kính ngữ (敬語) hoặc thân mật tùy tình huống
            7. Luôn kèm câu hỏi mở để tiếp tục hội thoại, phù hợp với chủ đề {topic}
            8. Đảm bảo câu trả lời có độ dài phù hợp với người học
            10. Không đính kèm icon, emoji, các kí tự đặc biệt
            11. Đảm bảo câu trả lời có thể sử dụng để tạo speech to text
            12. Khi đếm số lượng hội thoại đã diễn ra lớn hơn 5, chào tạm biệt và đề nghị người học có thể tiếp tục hội thoại vào lúc khác
            13. Vì là văn nói nên không bắt lỗi dấu câu
            
            Chỉ trả về JSON, không có văn bản giới thiệu hoặc kết luận.
            """
            
            # Generate content with Gemini
            response = self.model.generate_content(prompt)
            
            # Clean the response text to remove markdown or extra formatting
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            # Parse the JSON response
            try:
                response_json = json.loads(response_text)
                
                # Generate audio for the reply
                reply_text = response_json.get("reply", "")
                if reply_text:
                    audio_result = SpeechService.text_to_speech(reply_text, language='ja')
                    if audio_result["status"] == "success":
                        response_json["audio_reply"] = audio_result["audio_data"]
                    else:
                        response_json["audio_reply"] = None  # Or handle error differently
                        print(f"Error generating audio: {audio_result['message']}")
                
                # Save the conversation exchange
                new_exchange = {
                    "timestamp": datetime.now().isoformat(),
                    "topic": topic,
                    "user_level": user_level,
                    "user_input": user_input,
                    "correction": response_json.get("correction", {}),
                    "reply": response_json.get("reply", ""),
                    "vocabulary": response_json.get("vocabulary", [])
                }
                
                # Append to conversation history and save
                conversation_history.append(new_exchange)
                self._save_conversation_history(user_id, conversation_history)
                
                # Add audio_reply only to the response, not in history
                if audio_result and audio_result["status"] == "success":
                    response_json["audio_reply"] = audio_result["audio_data"]
                else:
                    response_json["audio_reply"] = None
                
                return {
                    "status": "success",
                    "user_id": user_id,
                    "response": response_json
                }
                
            except json.JSONDecodeError as json_err:
                return {
                    "status": "error",
                    "message": f"Invalid JSON response from AI: {str(json_err)}",
                    "raw_response": response_text
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def get_conversation_history(self, user_id, limit=10):
        """
        Get conversation history for a user
        
        Args:
            user_id (str): Unique identifier for the user
            limit (int): Maximum number of conversation exchanges to return
            
        Returns:
            dict: Result containing conversation history
        """
        try:
            history = self._load_conversation_history(user_id)
            
            # Return the most recent conversations up to the limit
            limited_history = history[-limit:] if limit > 0 else history
            
            return {
                "status": "success",
                "user_id": user_id,
                "conversation_history": limited_history
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}