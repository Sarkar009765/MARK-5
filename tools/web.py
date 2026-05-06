import requests
from tools.base import Tool, registry
from utils import logger

class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web"
    parameters = {
        "query": {"type": "string", "description": "Search query"},
        "max_results": {"type": "integer", "description": "Max results (default 5)"}
    }
    
    def execute(self, query: str, max_results: int = 5) -> str:
        try:
            # Using DuckDuckGo instant answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("Answer"):
                return data["Answer"]
            
            results = []
            for item in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(item, dict):
                    results.append(f"- {item.get('Text', '')}")
            
            return "\n".join(results) if results else "No results found"
        except Exception as e:
            return f"Search error: {e}"


class WeatherTool(Tool):
    name = "weather"
    description = "Get weather info"
    parameters = {
        "location": {"type": "string", "description": "City name"}
    }
    
    def execute(self, location: str = "") -> str:
        try:
            # Basic weather using wttr.in
            url = f"https://wttr.in/{location}?format=%c+%t+%h"
            response = requests.get(url, timeout=10)
            return response.text.strip()
        except Exception as e:
            return f"Weather unavailable: {e}"


class DictionaryTool(Tool):
    name = "define"
    description = "Define a word"
    parameters = {
        "word": {"type": "string", "description": "Word to define"}
    }
    
    def execute(self, word: str) -> str:
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()[0]
                meanings = data.get("meanings", [])[0]
                definition = meanings.get("definitions", [])[0]
                return definition.get("definition", "No definition found")
            return "Word not found"
        except Exception as e:
            return f"Error: {e}"


registry.register(WebSearchTool())
registry.register(WeatherTool())
registry.register(DictionaryTool())