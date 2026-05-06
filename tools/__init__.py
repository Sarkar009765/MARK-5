import re
import config
from tools.base import registry
from utils import logger
from typing import Dict, Any, Optional

# Import tools to register them
from tools import system
from tools import browser
from tools import files
from tools import web

class ToolExecutor:
    def __init__(self):
        self.registry = registry
        self.pending_confirmation: Optional[Dict] = None
    
    def parse_and_execute(self, user_input: str) -> str:
        user_lower = user_input.lower()
        
        # Web search
        if any(w in user_lower for w in ["search", "google", "find"]):
            query = user_input
            for w in ["search", "google", "find", "for"]:
                query = query.replace(w, "", 1)
            return self.execute_tool("web_search", {"query": query.strip()})
        
        # Weather
        if "weather" in user_lower or "তাপমাত্রা" in user_lower or "আবহাওয়া" in user_lower:
            return self.execute_tool("weather", {"location": ""})
        
        # Define/meaning
        if any(w in user_lower for w in ["define", "meaning", "ব্যাখ্যা", "অর্থ"]):
            word = user_input
            for w in ["define", "meaning", "of", "the", "word"]:
                word = re.sub(r'\b' + w + r'\b', '', word, flags=re.IGNORECASE)
            return self.execute_tool("define", {"word": word.strip()})
        
        # Open app
        if user_lower.startswith("open ") or user_lower.startswith("run "):
            app = user_input[5:]
            return self.execute_tool("open_app", {"app": app})
        
        # System info
        if "system" in user_lower or "cpu" in user_lower or "memory" in user_lower:
            return self.execute_tool("system_info", {})
        
        # Screenshot
        if "screenshot" in user_lower or "screenshot" in user_lower or "ছবি" in user_lower:
            return self.execute_tool("screenshot", {"path": ""})
        
        # Volume control
        if "volume" in user_lower or "sound" in user_lower or "ভলিউম" in user_lower:
            action = "up" if "up" in user_lower else ("down" if "down" in user_lower else "up")
            return self.execute_tool("volume", {"action": action})
        
        # List files
        if "list" in user_lower and "file" in user_lower:
            return self.execute_tool("list_files", {"path": "."})
        
        # Open URL
        if user_lower.startswith("open ") and ("http" in user_input or ".com" in user_input):
            return self.execute_tool("browser", {"url": user_input[5:]})
        
        return None
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return f"Tool {tool_name} not found"
        
        # Check confirmation
        if tool.requires_confirmation:
            self.pending_confirmation = {"tool": tool_name, "params": params}
            return f"Confirm: Execute {tool_name}?"
        
        try:
            result = tool.execute(**params)
            return result
        except Exception as e:
            logger.error(f"Tool error: {e}")
            return f"Error: {e}"
    
    def confirm(self) -> str:
        if not self.pending_confirmation:
            return "Nothing pending"
        
        tool_name = self.pending_confirmation["tool"]
        params = self.pending_confirmation["params"]
        self.pending_confirmation = None
        
        return self.execute_tool(tool_name, params)

    def cancel_confirmation(self):
        self.pending_confirmation = None
    
    def list_available_tools(self) -> str:
        tools = self.registry.list_tools()
        return "\n".join([f"- {t['name']}: {t['description']}" for t in tools])


tool_executor = ToolExecutor()