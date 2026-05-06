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

## Tech Stack

- LLM: Gemini 2.0 Flash (LiteLLM)
- STT: Vosk (tiny model)
- TTS: pyttsx3 (lightweight)
- Tools: Playwright, subprocess
- Memory: TinyDB

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python main.py
```

## Requirements

- Python 3.10+
- Windows 10/11
- ~2GB RAM free