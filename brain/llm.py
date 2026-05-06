import os
import json
import config
from brain.prompts import get_prompt, TOOL_SYSTEM_PROMPT
from memory.db import memory
from utils import logger
from tools import tool_executor

class Brain:
    def __init__(self):
        self.model = None
        self.chat = None
        self.language = config.LANGUAGE
        self._init_llm()
    
    def _init_llm(self):
        if config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(config.MODEL_NAME)
                logger.info(f"Gemini loaded: {config.MODEL_NAME}")
                self._init_chat()
            except Exception as e:
                logger.error(f"LLM init error: {e}")
    
    def _init_chat(self):
        if self.model:
            history = memory.get_conversations(config.MAX_MEMORY_MESSAGES)
            msgs = [{"role": m["role"], "parts": [m["content"]]} for m in history]
            self.chat = self.model.start_chat(history=msgs)

    def process(self, user_input: str) -> str:
        memory.add_message("user", user_input)
        
        tool_result = tool_executor.parse_and_execute(user_input)
        if tool_result:
            memory.add_message("model", tool_result)
            return tool_result
        
        if self.chat:
            try:
                response = self.chat.send_message(user_input)
                memory.add_message("model", response.text)
                return response.text
            except Exception as e:
                logger.error(f"LLM error: {e}")
                return self._fallback(user_input)
        
        return self._fallback(user_input)

    def _fallback(self, text: str) -> str:
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["hello", "hi", "হাই", "নমস্কার", "hey"]):
            return "Ah, good day to you too! How may I assist?"
        
        if any(w in text_lower for w in ["who are you", "তুমি কে", "your name"]):
            return "I am ClawVis, at your service."
        
        if any(w in text_lower for w in ["time", "সময়", "কয়টা"]):
            from datetime import datetime
            return f"It's {datetime.now().strftime('%I:%M %p')}."
        
        if any(w in text_lower for w in ["date", "তারিখ", "কোন দিন"]):
            from datetime import datetime
            return f"Today is {datetime.now().strftime('%B %d, %Y')}."
        
        if any(w in text_lower for w in ["help", "সাহায্য", "কিভাবে"]):
            tools = tool_executor.list_available_tools()
            return f"I can help with:\n{tools}"
        
        if any(w in text_lower for w in ["bye", "goodbye", "বিদায়"]):
            return "Toodles! Take care."
        
        return "I say, could you repeat that?"


brain = Brain()