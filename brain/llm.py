import google.generativeai as genai
import config
from brain.prompts import get_prompt
from memory.db import memory
from utils import logger

class Brain:
    def __init__(self):
        self.model = None
        self.chat = None
        self.language = config.LANGUAGE
        
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(config.MODEL_NAME)
            logger.info(f"Gemini model loaded: {config.MODEL_NAME}")
        
        self._init_chat()

    def _init_chat(self):
        if self.model:
            history = memory.get_conversations(config.MAX_MEMORY_MESSAGES)
            msgs = [{"role": m["role"], "parts": [m["content"]]} for m in history]
            self.chat = self.model.start_chat(history=msgs)

    def process(self, user_input: str) -> str:
        memory.add_message("user", user_input)
        
        if self.chat:
            try:
                response = self.chat.send_message(user_input)
                memory.add_message("model", response.text)
                return response.text
            except Exception as e:
                logger.error(f"Gemini error: {e}")
                return self._fallback_response(user_input)
        
        return self._fallback_response(user_input)

    def _fallback_response(self, text: str) -> str:
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["hello", "hi", "হাই", "নমস্কার"]):
            return "Ah, good day to you too! How may I assist?"
        
        if any(w in text_lower for w in ["who are you", "তুমি কে", "your name"]):
            return "I am ClawVis, at your service. Rather clever if I say so myself."
        
        if any(w in text_lower for w in ["time", "সময়", "কয়টা"]):
            from datetime import datetime
            return f"It's {datetime.now().strftime('%I:%M %p')}."
        
        if any(w in text_lower for w in ["date", "তারিখ", "কোন দিন"]):
            from datetime import datetime
            return f"Today is {datetime.now().strftime('%B %d, %Y')}."
        
        return "I say, could you repeat that? I'm still learning, old chap."


brain = Brain()