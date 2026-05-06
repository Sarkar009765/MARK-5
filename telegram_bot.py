import os
import asyncio
import config
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from utils import logger

class TelegramBot:
    def __init__(self, brain):
        self.brain = brain
        self.app = None
        self.running = False
        self.user_id = config.TELEGRAM_USER_ID

    def start(self):
        if not config.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram bot token not set")
            return
        
        self.running = True
        threading.Thread(target=self._run_async, daemon=True).start()
        logger.info("Telegram bot starting...")

    def _run_async(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._start_bot())
        except Exception as e:
            logger.error(f"Telegram error: {e}")

    async def _start_bot(self):
        self.app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("voice", self.voice_command))
        self.app.add_handler(CommandHandler("sync", self.sync_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        self.app.run_polling(drop_pending_updates=True)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "ClawVis Telegram Bot activated!\n"
            "I'm connected to your PC assistant.\n"
            "Use /help for commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Commands:\n"
            "/start - Start bot\n"
            "/help - Show this help\n"
            "/status - System status\n"
            "/voice - Activate voice mode\n"
            "/sync - Sync conversations\n"
            "\nOr just text me!"
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from tools.system import SystemInfoTool
        tool = SystemInfoTool()
        status = tool.execute()
        await update.message.reply_text(f"System:\n{status}")

    async def voice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Voice activation triggered on PC!")
        from voice.tts import tts
        tts.speak_async("Voice mode activated. How may I help?")

    async def sync_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Syncing conversation history...")
        from memory.db import memory
        convos = memory.get_conversations(10)
        await update.message.reply_text(f"Recent: {len(convos)} messages")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if str(update.message.from_user.id) != self.user_id and self.user_id:
            logger.warning(f"Unauthorized user: {update.message.from_user.id}")
            return
        
        user_text = update.message.text
        logger.info(f"Telegram: {user_text}")
        
        response = self.brain.process(user_text)
        logger.info(f"Response: {response[:100]}...")
        
        await update.message.reply_text(response)

    def send_message(self, text: str):
        if not self.app or not self.user_id:
            return
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                self.app.bot.send_message(chat_id=self.user_id, text=text)
            )
        except Exception as e:
            logger.error(f"Send message error: {e}")

    def stop(self):
        self.running = False
        if self.app:
            self.app.stop()


telegram_bot = None

def init_telegram(brain):
    global telegram_bot
    telegram_bot = TelegramBot(brain)
    return telegram_bot