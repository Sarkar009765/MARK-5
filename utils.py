import logging
import sys
from pathlib import Path
import config

def setup_logger(name: str = "ClawVis") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    return logger

logger = setup_logger()

def get_resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.resolve()
    return base_path / relative_path

def load_json_file(filepath: Path):
    import json
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json_file(filepath: Path, data: dict):
    import json
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def format_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def get_clipboard_text() -> str:
    try:
        import pyperclip
        return pyperclip.paste()
    except Exception:
        return ""

def set_clipboard_text(text: str):
    try:
        import pyperclip
        pyperclip.copy(text)
    except Exception:
        pass