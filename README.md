# ClawVis - Personal AI Assistant

Version: 1.0 | May 2026

ClawVis is an ultra-lightweight personal AI agent that runs on your PC with ≤2.2GB RAM.

## Features

- Wake word voice activation ("Jarvis")
- British-style witty personality
- Computer control (apps, browser, files)
- Telegram bot integration
- Proactive notifications
- Simple self-learning
- Auto-start on boot

## Tech Stack

- LLM: Gemini 2.0 Flash
- TTS: pyttsx3 (lightweight)
- Tools: subprocess, pyautogui
- Memory: TinyDB

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python main.py
```

## Configuration (.env)

```
GEMINI_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_USER_ID=your_user_id
```

## Voice Commands

- Say "Jarvis" to activate
- "Search [query]" - Web search
- "Open [app]" - Open application
- "System info" - Check CPU/memory
- "Screenshot" - Take screenshot
- "Volume up/down" - Control volume

## Telegram Commands

- /start - Start bot
- /help - Show help
- /status - System status
- /voice - Activate voice mode

## Auto-Start

Run `scripts\auto_start.bat` to enable auto-start on Windows boot.

## Building .exe

```bash
pip install pyinstaller
pyinstaller clawvis.spec
```

## Requirements

- Python 3.10+
- Windows 10/11
- ~2GB RAM free
- Internet for API calls

## License

MIT