import os
import subprocess
import psutil
from tools.base import Tool, registry
from utils import logger
from typing import Optional

class OpenAppTool(Tool):
    name = "open_app"
    description = "Open an application by name or path"
    parameters = {
        "app": {"type": "string", "description": "App name or path"}
    }
    
    def execute(self, app: str) -> str:
        try:
            subprocess.Popen(app, shell=True)
            return f"Opening {app}..."
        except Exception as e:
            return f"Error opening {app}: {e}"


class CloseAppTool(Tool):
    name = "close_app"
    description = "Close an application by name"
    parameters = {
        "app": {"type": "string", "description": "App name to close"}
    }
    requires_confirmation = True
    
    def execute(self, app: str) -> str:
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == app.lower() + '.exe':
                    proc.terminate()
                    return f"Closed {app}"
            return f"{app} not found"
        except Exception as e:
            return f"Error closing {app}: {e}"


class ListProcessesTool(Tool):
    name = "list_processes"
    description = "List running processes"
    
    def execute(self) -> str:
        procs = []
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                procs.append(f"{proc.info['name']} ({proc.info['cpu_percent']}%)")
            except:
                pass
        return "\n".join(procs[:20])


class VolumeTool(Tool):
    name = "volume"
    description = "Control system volume"
    parameters = {
        "action": {"type": "string", "enum": ["up", "down", "mute", "unmute"]}
    }
    
    def execute(self, action: str = "up") -> str:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            if action == "up":
                volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() + 0.1, None)
            elif action == "down":
                volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() - 0.1, None)
            elif action == "mute":
                volume.SetMute(True, None)
            elif action == "unmute":
                volume.SetMute(False, None)
            
            return f"Volume {action}"
        except Exception as e:
            return f"Volume control not available: {e}"


class ScreenshotTool(Tool):
    name = "screenshot"
    description = "Take a screenshot"
    parameters = {
        "path": {"type": "string", "description": "Save path (optional)"}
    }
    
    def execute(self, path: str = "") -> str:
        try:
            import pyautogui
            if not path:
                path = "screenshot.png"
            pyautogui.screenshot().save(path)
            return f"Screenshot saved to {path}"
        except Exception as e:
            return f"Screenshot failed: {e}"


class SystemInfoTool(Tool):
    name = "system_info"
    description = "Get system information"
    
    def execute(self) -> str:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            return (f"CPU: {cpu}%\n"
                    f"Memory: {mem.percent}% used\n"
                    f"Disk: {disk.percent}% used")
        except Exception as e:
            return f"Error: {e}"


# Register tools
registry.register(OpenAppTool())
registry.register(CloseAppTool())
registry.register(ListProcessesTool())
registry.register(VolumeTool())
registry.register(ScreenshotTool())
registry.register(SystemInfoTool())