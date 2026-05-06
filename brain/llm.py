import os
import json
import config
from brain.prompts import get_prompt, TOOL_SYSTEM_PROMPT
from memory.db import memory
from utils import logger
from tools import tool_executor
from learning import learning

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
                
                system_prompt = get_prompt(self.language) + "\n" + TOOL_SYSTEM_PROMPT
                self.model = genai.GenerativeModel(
                    config.MODEL_NAME,
                    system_instruction=system_prompt
                )
                logger.info(f"Gemini loaded: {config.MODEL_NAME}")
                self._init_chat()
            except Exception as e:
                logger.error(f"LLM init error: {e}")
        else:
            logger.warning("No Gemini API key set. Running in offline mode.")
    
    def _init_chat(self):
        if self.model:
            history = memory.get_conversations(config.MAX_MEMORY_MESSAGES)
            msgs = [{"role": m["role"], "parts": [m["content"]]} for m in history]
            self.chat = self.model.start_chat(history=msgs)

    def process(self, user_input: str) -> str:
        memory.add_message("user", user_input)
        
        # 1. Check if it's a tool command first
        tool_result = tool_executor.parse_and_execute(user_input)
        if tool_result:
            memory.add_message("model", tool_result)
            learning.learn(user_input, tool_result)
            return tool_result
        
        # 2. Check if learning module has a good cached response
        learned_response = learning.get_best_response(user_input)
        feedback_score = learning.get_feedback(user_input, learned_response) if learned_response else -1
        
        # Use learned response only if it has positive feedback (score > 2)
        if learned_response and feedback_score > 2:
            logger.info(f"Using learned response (score: {feedback_score})")
            memory.add_message("model", learned_response)
            return learned_response
        
        # 3. Try Gemini (primary LLM)
        if self.chat:
            try:
                response = self.chat.send_message(user_input)
                result = response.text
                memory.add_message("model", result)
                learning.learn(user_input, result)
                return result
            except Exception as e:
                logger.error(f"Gemini error: {e}")
        
        # 4. Try fallback LLMs (Grok, DeepSeek)
        fallback_result = self._try_fallback_llms(user_input)
        if fallback_result:
            memory.add_message("model", fallback_result)
            learning.learn(user_input, fallback_result)
            return fallback_result
        
        # 5. Last resort: hardcoded responses
        result = self._hardcoded_fallback(user_input)
        memory.add_message("model", result)
        return result

    def _try_fallback_llms(self, text: str) -> str:
        """Try Grok and DeepSeek as fallback LLMs."""
        system_prompt = get_prompt(self.language)
        
        # Try Grok (xAI API)
        if config.GROK_API_KEY:
            try:
                import requests
                response = requests.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.GROK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-2",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": text}
                        ],
                        "max_tokens": 500
                    },
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    result = data["choices"][0]["message"]["content"]
                    logger.info("Grok fallback succeeded")
                    return result
            except Exception as e:
                logger.error(f"Grok fallback error: {e}")
        
        # Try DeepSeek
        if config.DEEPSEEK_API_KEY:
            try:
                import requests
                response = requests.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": text}
                        ],
                        "max_tokens": 500
                    },
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    result = data["choices"][0]["message"]["content"]
                    logger.info("DeepSeek fallback succeeded")
                    return result
            except Exception as e:
                logger.error(f"DeepSeek fallback error: {e}")
        
        return None

    def _hardcoded_fallback(self, text: str) -> str:
        """Last resort when no LLM is available."""
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
        
        return "I'm running without an AI brain at the moment. Please set up a Gemini API key in .env file."


brain = Brain()