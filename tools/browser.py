import os
import asyncio
from tools.base import Tool, registry
from utils import logger

class BrowserTool(Tool):
    name = "browser"
    description = "Open URL in default browser"
    parameters = {
        "url": {"type": "string", "description": "URL to open"}
    }
    
    def execute(self, url: str) -> str:
        try:
            import webbrowser
            webbrowser.open(url)
            return f"Opened {url}"
        except Exception as e:
            return f"Error: {e}"


class PlaywrightTool(Tool):
    name = "browser_control"
    description = "Control browser with Playwright"
    parameters = {
        "action": {"type": "string", "enum": ["open", "screenshot", "get_html"]},
        "url": {"type": "string", "description": "URL for action"}
    }
    
    def __init__(self):
        super().__init__()
        self.browser = None
        self.page = None
    
    async def _async_execute(self, action: str, url: str = "") -> str:
        try:
            from playwright.async_api import async_playwright
            
            if action == "open":
                webbrowser.open(url)
                return f"Opened {url}"
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url)
                
                if action == "screenshot":
                    await page.screenshot(path="screenshot.png")
                    await browser.close()
                    return "Screenshot saved"
                
                elif action == "get_html":
                    html = await page.content()
                    await browser.close()
                    return html[:1000]
                
                await browser.close()
                return "Done"
        except Exception as e:
            return f"Error: {e}"
    
    def execute(self, action: str = "open", url: str = "") -> str:
        try:
            return asyncio.run(self._async_execute(action, url))
        except Exception as e:
            return f"Browser error: {e}"


registry.register(BrowserTool())
registry.register(PlaywrightTool())