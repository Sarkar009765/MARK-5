import config
from utils import logger
from typing import Any, Dict, Optional

class Tool:
    name: str = ""
    description: str = ""
    parameters: Dict = {}
    requires_confirmation: bool = False
    
    def __init__(self):
        self.last_result: Optional[str] = None
    
    def execute(self, **kwargs) -> str:
        raise NotImplementedError
    
    def validate_params(self, params: dict) -> bool:
        return True
    
    def format_result(self, result: Any) -> str:
        if isinstance(result, str):
            return result
        return str(result)


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        return [
            {
                "name": t.name,
                "description": t.description,
                "requires_confirmation": t.requires_confirmation
            }
            for t in self.tools.values()
        ]


registry = ToolRegistry()