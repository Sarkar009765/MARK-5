# ClawVis

**Ultra-Lightweight Personal AI Agent**  
*Jarvis × OpenClaw × Hermes × Paperclip*

A smart, proactive, voice-enabled personal AI that runs smoothly on low-end PCs (even 4GB RAM).

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)

## ✨ Features

- **Voice Interaction** — Wake word "Jarvis" with natural conversation
- **Proactive Assistant** — Paperclip-style suggestions and reminders
- **Real Computer Control** — Open apps, control browser, file management, web research
- **Telegram Bot** — Control from mobile
- **Multi-Language** — English + Bengali
- **Self-Learning** — Learns from your usage
- **Ultra Lightweight** — Runs on 4GB RAM PCs

## 🛠️ Tech Stack

- **Brain**: LiteLLM + Gemini 2.5 Flash (with fallback)
- **Voice**: Vosk (STT) + Piper TTS
- **Tools**: Playwright, subprocess
- **Memory**: TinyDB + JSON
- **Interface**: Local Voice + Telegram

## 📁 Project Structure

```bash
clawvis/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── voice/
├── brain/
├── tools/
├── memory/
├── notifications.py
├── telegram_bot.py
├── utils.py
├── scripts/
└── docs/
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git
- Microphone (for voice)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Sarkar009765/MARK-5.git
cd MARK-5

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
copy .env.example .env
# Edit .env file and add your Gemini API key
```

### Run

```bash
python main.py
```

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome!

---

Made with ❤️ for low-end PCs